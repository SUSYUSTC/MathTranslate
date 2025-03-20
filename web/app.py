from flask import Flask, render_template, request, send_from_directory, redirect, flash, Response
import os
import subprocess
import werkzeug
import shutil
import sched
import time
import zipfile
import glob
import uuid
from datetime import datetime
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'  # USE data as working dir
app.config['ALLOWED_EXTENSIONS'] = {'tex'}
app.secret_key = "some_secret_key"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def stream_file(uid):
    """Continuously stream the full file content every second."""
    while True:
        filename = f"output/{uid}"
        content = open(filename, "r").read().strip()
        formatted_content = "\n".join(f"data: {line}" for line in content.split("\n"))
        yield f"{formatted_content}\n\n"
        #yield f"data: {content}\n\n"  # SSE format

        time.sleep(0.2)  # Avoid excessive CPU usage


def return_new_index():
    uid = str(uuid.uuid4())
    filename = f"output/{uid}"
    open(filename, "w").close()
    return render_template('index.html', uid=uid, translated=False)


@app.route('/stream')
def stream():
    uid = request.args.get("uid")
    print('requested', uid)
    return Response(stream_file(uid), mimetype='text/event-stream')


def translate_arxiv(uid):
    has_zip = False
    has_pdf = False
    zipname = ""
    pdfname = ""

    arxiv_id = request.form['arxiv_id']
    input_lang = request.form['inputLanguageCode']
    output_lang = request.form['outputLanguageCode']
    if not arxiv_id:
        flash("Please enter an Arxiv ID.")
        return return_new_index()

    arxiv_id1 = arxiv_id.replace('/', '-')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], arxiv_id1)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open("logging", "a") as f:
        print(datetime.now(), file=f)
        print(folder_path, file=f)
        print(arxiv_id1, file=f)
    # Try to generate arxiv_id.zip
    f = open(f"output/{uid}", "w")
    process = subprocess.run(
        ['translate_arxiv', arxiv_id, '-from', input_lang, '-to', output_lang], cwd=folder_path, stdout=f, stderr=f, text=True, timeout=300)
    f.close()

    # replace '/'
    arxiv_id = arxiv_id.replace('/', '-')

    # If the process failed, return error, can be optimized with more precise failed signal
    time.sleep(1)
    '''
    end_time = time.time() + 3
    while time.time() < end_time:
        if os.path.exists(os.path.join(folder_path, f"{arxiv_id}.zip")):
            break
        time.sleep(0.5)
    '''

    # If after 30 seconds the zip file is still not found, flash an error message
    if not os.path.exists(os.path.join(folder_path, f"{arxiv_id}.zip")):
        flash("An error incurred. Please see the program output for details")
        return render_template('index.html', uid=uid, translated=False)

    # Set zipname here as the .zip file exists
    has_zip = True
    zipname = f"{arxiv_id}.zip"

    # Copy the .zip file to the main UPLOAD_FOLDER directory
    shutil.copy(os.path.join(folder_path, f"{arxiv_id}.zip"), os.path.join(
        app.config['UPLOAD_FOLDER'], f"{arxiv_id}.zip"))

    # Unzip the file
    with zipfile.ZipFile(os.path.join(folder_path, f"{arxiv_id}.zip"), 'r') as zip_ref:
        zip_ref.extractall(folder_path)

    # Check for .tex files in the folder
    tex_files = glob.glob(os.path.join(folder_path, "*.tex"))

    if not tex_files:  # If no .tex files are found
        flash("No .tex files found. The paper might not be supported.")
        return render_template('index.html', uid=uid, translated=False)

    # Choose the main.tex file if it exists, otherwise choose the first .tex file
    if os.path.join(folder_path, 'main.tex') in tex_files:
        tex_to_compile = 'main.tex'
    else:
        # Get the name of the first .tex file
        tex_to_compile = os.path.basename(tex_files[0])

    latex_log_file = open(os.path.join(folder_path, 'latex_log'), "w")
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    tex_to_compile], cwd=folder_path, stdout=latex_log_file)  # Initial compilation
    subprocess.run(['bibtex', tex_to_compile.rsplit('.', 1)[
                    0]], cwd=folder_path, stdout=latex_log_file)  # Run bibtex for references
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    tex_to_compile], cwd=folder_path, stdout=latex_log_file)  # Second compilation
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    tex_to_compile], cwd=folder_path, stdout=latex_log_file)  # Third compilation

    # Check if the .pdf version of the compiled .tex exists
    if os.path.exists(os.path.join(folder_path, tex_to_compile.rsplit('.', 1)[0] + '.pdf')):
        has_pdf = True
        pdfname = f"{arxiv_id}.pdf"

        # Rename and move the file
        os.rename(os.path.join(folder_path, tex_to_compile.rsplit('.', 1)[
                    0] + '.pdf'), os.path.join(app.config['UPLOAD_FOLDER'], f"{arxiv_id}.pdf"))
    else:
        has_pdf = False
        pdfname = ""
        flash('PDF generation failed. Please try on Overleaf. You can directly upload the zip file. You must set the compiler to XeLaTeX otherwise it would fail.')
    if has_pdf or has_zip:
        return render_template('index.html', uid=uid, has_pdf=has_pdf, has_zip=has_zip, pdfname=pdfname, zipname=zipname)
    else:
        return render_template('index.html', uid=uid, translated=False)


def upload_zip(uid):
    has_zip = False
    has_pdf = False
    zipname = ""
    pdfname = ""
    # Check if a file is present
    if 'zip_file' not in request.files:
        flash('No file part')
        return return_new_index()

    zip_file = request.files['zip_file']
    input_lang = request.form['inputLanguageCode']
    output_lang = request.form['outputLanguageCode']

    # If no file is selected
    if zip_file.filename == '':
        flash('No selected file')
        return render_template('index.html', translated=False)

    # Save the ZIP file
    zipname = werkzeug.utils.secure_filename(zip_file.filename)
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zipname)
    zip_file.save(zip_path)

    # Extract the ZIP file to a specific folder
    extract_folder = os.path.join(
        app.config['UPLOAD_FOLDER'], zipname.rsplit('.', 1)[0])
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Check for .tex files in the folder
    tex_files = glob.glob(os.path.join(extract_folder, "*.tex"))

    if not tex_files:  # If no .tex files are found
        flash("No .tex files found. The ZIP might not be supported.")
        return return_new_index()

    # Choose the main.tex file if it exists, otherwise choose the first .tex file
    if os.path.join(extract_folder, 'main.tex') in tex_files:
        tex_to_compile = 'main.tex'
    else:
        # Get the name of the first .tex file
        tex_to_compile = os.path.basename(tex_files[0])

    # Translate the chosen .tex file
    output_filename = tex_to_compile.rsplit('.', 1)[0] + "_out.tex"
    f = open(f"output/{uid}", "w")
    process = subprocess.run(['translate_tex', tex_to_compile, '-o', output_filename,
                    '-from', input_lang, '-to', output_lang], cwd=extract_folder,
                             stdout=f, stderr=f, text=True, timeout=30)
    f.close()

    # Run xelatex to generate the PDF with bibtex for references using the translated .tex file
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    output_filename], cwd=extract_folder)  # Initial compilation
    subprocess.run(['bibtex', output_filename.rsplit('.', 1)[
                    0]], cwd=extract_folder)  # Run bibtex for references
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    output_filename], cwd=extract_folder)  # Second compilation
    subprocess.run(['xelatex', '-interaction=nonstopmode',
                    output_filename], cwd=extract_folder)  # Third compilation

    # Check if the .pdf version of the compiled .tex exists
    if os.path.exists(os.path.join(extract_folder, output_filename.rsplit('.', 1)[0] + '.pdf')):
        has_pdf = True
        pdfname = f"{zipname.rsplit('.', 1)[0]}.pdf"

        # Rename and move the file
        os.rename(os.path.join(extract_folder, output_filename.rsplit('.', 1)[
                    0] + '.pdf'), os.path.join(app.config['UPLOAD_FOLDER'], pdfname))
    else:
        flash('Compile Error. Please try on Overleaf. You can directly upload the zip file. You must set the compiler to XeLaTeX otherwise it would fail.')
        return render_template('index.html', uid=uid, translated=False)
    if has_pdf or has_zip:
        return render_template('index.html', uid=uid, has_pdf=has_pdf, has_zip=has_zip, pdfname=pdfname, zipname=zipname)
    else:
        return render_template('index.html', uid=uid, translated=False)


def upload_translate(uid):
    has_zip = False
    has_pdf = False
    zipname = ""
    pdfname = ""
    input_lang = request.form['inputLanguageCode']
    output_lang = request.form['outputLanguageCode']
    # Check if a file is present
    if 'file' not in request.files:
        flash('No file part')
        return return_new_index()

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        flash('No selected file')
        return return_new_index()

    # file is allowed
    if file and allowed_file(file.filename):
        filename = werkzeug.utils.secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # check files with same name
        if os.path.exists(filepath):
            os.remove(filepath)
            # delete _out.tex
            output_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0] + "_out.tex")
            if os.path.exists(output_filepath):
                os.remove(output_filepath)

        file.save(filepath)

        # translate
        output_filename = filename.rsplit('.', 1)[0] + "_out.tex"
        f = open(f"output/{uid}", "w")
        process = subprocess.run(['translate_tex', filename, '-o', output_filename,
                        '-from', input_lang, '-to', output_lang], cwd=app.config['UPLOAD_FOLDER'],
                                 stdout=f, stderr=f, text=True, timeout=30)
        f.close()
        # generate pdf
        pdf_filename = output_filename.replace(".tex", ".pdf")
        subprocess.run(['xelatex', '-interaction=nonstopmode',
                        output_filename], cwd=app.config['UPLOAD_FOLDER'])

        return render_template('index.html', uid=uid, translated=True, tex_filename=output_filename, pdf_filename=pdf_filename)
    if has_pdf or has_zip:
        return render_template('index.html', uid=uid, has_pdf=has_pdf, has_zip=has_zip, pdfname=pdfname, zipname=zipname)
    else:
        return render_template('index.html', uid=uid, translated=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Variables to track if we have a ZIP or PDF file

        # Check if the "Translate arxiv" button was clicked
        if 'translate_arxiv' in request.form:
            uid = request.form['uid']
            return translate_arxiv(uid)
        elif 'upload_zip' in request.form:
            uid = request.form['uid']
            return upload_zip(uid)
        elif 'upload_translate' in request.form:
            uid = request.form['uid']
            return upload_translate(uid)

    return return_new_index()


@app.route('/<filename>')
def uploaded_file(filename):
    response = send_from_directory(
        app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    return response


s = sched.scheduler(time.time, time.sleep)


def delete_files_from_data_directory(sc):
    data_path = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Schedule the function to be run again in 3600 seconds (1 hour)
    s.enter(3600, 1, delete_files_from_data_directory, (sc,))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
