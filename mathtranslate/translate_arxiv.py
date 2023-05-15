from . import utils
from . import process_latex
from . import process_file
from .translate import translate_single_tex_file
from .encoding import get_file_encoding
import os
import sys
import shutil
import gzip
import zipfile
import tarfile
import tempfile
import urllib.request


def download_source(number):
    url = f'https://arxiv.org/e-print/{number}'
    urllib.request.urlretrieve(url, number)


def is_pdf(filename):
    return open(filename, 'rb').readline()[0:4] == b'%PDF'


def loop_files(dir):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def zipdir(dir, output_path):
    # ziph is zipfile handle
    zipf = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    for file in loop_files(dir):
        rel_path = os.path.relpath(file, dir)
        zipf.write(file, arcname=rel_path)


def translate_dir(dir, options):
    files = loop_files(dir)
    texs = [f[0:-4] for f in files if f[-4:] == '.tex']
    bibs = [f[0:-4] for f in files if f[-4:] == '.bib']
    bbls = [f[0:-4] for f in files if f[-4:] == '.bbl']
    no_bib = len(bibs) == 0
    print('main tex files found:')
    complete_texs = []
    for tex in texs:
        path = f'{tex}.tex'
        input_encoding = get_file_encoding(path)
        content = open(path, encoding=input_encoding).read()
        content = process_latex.remove_tex_comments(content)
        complete = process_latex.is_complete(content)
        if complete:
            process_file.merge_complete(tex)
            if no_bib and (tex in bbls):
                process_file.add_bbl(tex)
            complete_texs.append(tex)
            print(path)
    if len(complete_texs) == 0:
        return False
    for basename in texs:
        if basename in complete_texs:
            continue
        os.remove(f'{basename}.tex')
    for basename in bbls:
        os.remove(f'{basename}.bbl')
    for filename in complete_texs:
        print(f'Processing {filename}')
        file_path = f'{filename}.tex'
        translate_single_tex_file(file_path, file_path, options.engine, options.l_from, options.l_to, options.debug)
    return True


def main(args=None, require_updated=True):
    '''
    There are four types of a downdload arxiv project
    1. It is simply a PDF file (cannot translate)
    2. It is a gzipped text file, but the text file contains nothing meaningful (cannot translate)
    3. It is a gzipped tex file (can translate)
    4. It is a gzipped + tarzipped tex project (can translate)

    return False for the first two cases
    return True if the translation is successful (last two cases)

    to call this function from python,
    you can do e.g `arxiv(['2205.15510', '-o', 'output.zip'])`
    '''
    utils.check_update(require_updated=require_updated)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("number", nargs='?', type=str, help='arxiv number')
    parser.add_argument("-o", type=str, help='output path')
    utils.add_arguments(parser)
    options = parser.parse_args(args)
    utils.process_options(options)

    if options.number is None:
        parser.print_help()
        sys.exit()

    number = options.number
    if options.o is None:
        output_path = f'{number}.zip'
    else:
        output_path = options.o

    success = True
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        print('temporary directory', temp_dir)
        os.chdir(temp_dir)
        try:
            download_source(number)
        except urllib.error.HTTPError:
            print(f'Specified arxiv {number} not found')
            return False
        except BaseException:
            print('Cannot download source, maybe network issue')
            return False
        if is_pdf(number):
            # case 1
            success = False
        content = gzip.decompress(open(number, "rb").read())
        with open(number, "wb") as f:
            f.write(content)
        try:
            # case 4
            with tarfile.open(number, mode='r') as f:
                f.extractall()
            os.remove(number)
        except tarfile.ReadError:
            # case 2 or 3
            print('This is a pure text file')
            shutil.move(number, 'main.tex')
        success = translate_dir('.', options)
        if not success:
            # case 2
            success = False
        os.chdir(cwd)
        zipdir(temp_dir, output_path)

    if success:
        print('zip file is saved to', output_path)
        print('You can upload the zip file to overleaf to autocompile')
        return True
    else:
        print('Source code is not available in arxiv', number)
        return False
