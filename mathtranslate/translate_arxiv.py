from . import main, utils
import os
import subprocess
import sys
import gzip
import tarfile
import urllib.request


def download_source(number):
    url = f'https://arxiv.org/e-print/{number}'
    urllib.request.urlretrieve(url, number)


def is_pdf(filename):
    return open(filename, 'rb').readline()[0:4] == b'%PDF'


def translate_dir():
    files = os.listdir('./')
    texs = [f[0:-4] for f in files if f[-4:] == '.tex']
    bibs = [f[0:-4] for f in files if f[-4:] == '.bib']
    bbls = [f[0:-4] for f in files if f[-4:] == '.bbl']
    no_bib = len(bibs) == 0
    print('tex files found:')
    for tex in texs:
        print(tex)
    for filename in texs:
        print(f'Processing {filename}')
        if no_bib and (filename in bbls):
            args = utils.split(f'{filename}.tex -insertbbl {filename.bbl} --overwrite')
        else:
            args = utils.split(f'{filename}.tex --overwrite')
        main(args)


def arxiv(number):
    download_source(number)
    if is_pdf(number):
        print('The latex source is not provided for this paper. Cannot translate.')
        sys.exit()
    content = gzip.decompress(open(number, "rb").read())
    with open(number, "wb") as f:
        f.write(content)
    with tarfile.open(number, mode='r') as f:
        f.extractall()
    translate_dir()
