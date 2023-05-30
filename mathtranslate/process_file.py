import os
import re
from .process_latex import remove_tex_comments
from .encoding import get_file_encoding


def merge_complete(tex):
    '''
    for replace all \input commands by the file content
    '''
    path = f'{tex}.tex'
    dirname = os.path.dirname(path)
    encoding = get_file_encoding(path)
    content = open(path, encoding=encoding).read()
    content = remove_tex_comments(content)
    pattern_input = re.compile(r'\\input{(.*?)}')
    while True:
        result = pattern_input.search(content)
        if result is None:
            break
        begin, end = result.span()
        match = result.group(1)
        filename = os.path.join(dirname, match)
        if os.path.exists(f'{filename}.tex'):
            filename = f'{filename}.tex'
        print('merging', filename)
        assert os.path.exists(filename)
        encoding = get_file_encoding(filename)
        new_content = open(filename, encoding=encoding).read()
        new_content = remove_tex_comments(new_content)
        content = content[:begin] + new_content + content[end:]
    print(content, file=open(path, "w", encoding='utf-8'))


def add_bbl(tex):
    '''
    for replace \bibliography commands by the corresponding bbl file
    '''
    path_tex = f'{tex}.tex'
    path_bbl = f'{tex}.bbl'
    encoding = get_file_encoding(path_tex)
    content = open(path_tex, encoding=encoding).read()
    encoding = get_file_encoding(path_bbl)
    bbl = open(path_bbl, encoding=encoding).read()
    pattern_input = re.compile(r'\\bibliography\{(.*?)\}', re.DOTALL)
    while True:
        result = pattern_input.search(content)
        if result is None:
            break
        begin, end = result.span()
        content = content[:begin] + bbl + content[end:]
    print(content, file=open(path_tex, "w", encoding='utf-8'))
