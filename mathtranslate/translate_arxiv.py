from . import utils
from . import process_latex
from . import process_file
from .translate import translate_single_tex_file
from .encoding import get_file_encoding
from . import app_dir
import os
import sys
import shutil
import gzip
import zipfile
import tarfile
import tempfile
import urllib.request


def download_source(number, path):
    url = f'https://arxiv.org/e-print/{number}'
    print('trying to download from', url)
    urllib.request.urlretrieve(url, path)


def download_source_with_cache(number, path):
    cache_dir = os.path.join(app_dir, 'cache_arxiv')
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, 'last_downloaded_source')
    cache_number_path = os.path.join(cache_dir, 'last_arxiv_number')
    if os.path.exists(cache_path) and os.path.exists(cache_number_path):
        last_number = open(cache_number_path).read()
        if last_number == number:
            shutil.copyfile(cache_path, path)
            return
    download_source(number, path)
    shutil.copyfile(path, cache_path)
    open(cache_number_path, 'w').write(number)


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
            print(path)
            process_file.merge_complete(tex)
            if no_bib and (tex in bbls):
                process_file.add_bbl(tex)
            complete_texs.append(tex)
    if len(complete_texs) == 0:
        return False
    for basename in texs:
        if basename in complete_texs:
            continue
        os.remove(f'{basename}.tex')
    for basename in bbls:
        os.remove(f'{basename}.bbl')
    if options.notranslate:
        return True
    for filename in complete_texs:
        print(f'Processing {filename}')
        file_path = f'{filename}.tex'
        translate_single_tex_file(file_path, file_path, options.engine, options.l_from, options.l_to, options.debug, options.nocache, options.threads)
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
    you can do e.g `main(['2205.15510', '-o', 'output.zip'])`
    '''
    utils.check_update(require_updated=require_updated)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("number", nargs='?', type=str, help='arxiv number')
    parser.add_argument("-o", type=str, help='output path')
    parser.add_argument("--from_dir", action='store_true')
    parser.add_argument("--notranslate", action='store_true')  # debug option
    utils.add_arguments(parser)
    options = parser.parse_args(args)
    utils.process_options(options)

    if options.number is None:
        parser.print_help()
        sys.exit()

    number = options.number
    print('arxiv number:', number)
    print()
    download_path = number.replace('/', '-')
    if options.o is None:
        output_path = f'{download_path}.zip'
    else:
        output_path = options.o

    success = True
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        print('temporary directory', temp_dir)
        if options.from_dir:
            shutil.copytree(number, temp_dir, dirs_exist_ok=True)
        os.chdir(temp_dir)
        # must os.chdir(cwd) whenever released!
        try:
            if not options.from_dir:
                try:
                    download_source_with_cache(number, download_path)
                except BaseException:
                    print('Cannot download source, maybe network issue or wrong link')
                    os.chdir(cwd)
                    return False
                if is_pdf(download_path):
                    # case 1
                    success = False
                else:
                    content = gzip.decompress(open(download_path, "rb").read())
                    with open(download_path, "wb") as f:
                        f.write(content)
                    try:
                        # case 4
                        with tarfile.open(download_path, mode='r') as f:
                            f.extractall()
                        os.remove(download_path)
                    except tarfile.ReadError:
                        # case 2 or 3
                        print('This is a pure text file')
                        shutil.move(download_path, 'main.tex')
                    success = translate_dir('.', options)
            else:
                success = translate_dir('.', options)
            os.chdir(cwd)
            if success:
                # case 3 or 4
                zipdir(temp_dir, output_path)
        except BaseException as e:
            # first go back otherwise tempfile trying to delete the current directory that python is running in
            os.chdir(cwd)
            raise e

    if success:
        print('zip file is saved to', output_path)
        print('You can upload the zip file to overleaf to autocompile')
        return True
    else:
        print('Source code is not available for arxiv', number)
        return False
