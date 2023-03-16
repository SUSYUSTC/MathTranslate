#!/usr/bin/env python
import os
import sys
import mtranslate
language_from = 'en'
language_to = 'zh-CN'
# the code list for languages can be obtained by running "trans -R" in your terminal


def is_connected(line_above, line_below):
    if len(line_above) > 0 and len(line_below) > 0:
        if line_above[-1] != '.' and line_below[0].islower():
            return True
    return False


def connect_paragraphs(text):
    text_split = text.split('\n')
    i = 0
    while i < len(text_split) - 1:
        line_above = text_split[i]
        line_below = text_split[i + 1]
        if is_connected(line_above, line_below):
            text_split[i] = text_split[i] + text_split[i + 1]
            del text_split[i + 1]
        else:
            i += 1
    return '\n'.join(text_split)


def is_title(line_above, line_below):
    if len(line_above) > 0 and len(line_below) > 0:
        if line_above[-1] != '.' and line_above[0].isupper() and line_below[0].isupper():
            return True
    return False


def split_titles(text):
    text_split = text.split('\n')
    i = 0
    while i < len(text_split) - 1:
        line_above = text_split[i]
        line_below = text_split[i + 1]
        if is_title(line_above, line_below):
            text_split[i] = '\n\n' + text_split[i] + '\n\n'
        i += 1
    return '\n'.join(text_split)


def convert_next(text, pattern_begin, pattern_end, count):
    position_begin = text.find(pattern_begin)
    position_end = text.find(pattern_end)
    l = len(pattern_end)
    assert not ((position_begin == -1) ^ (position_end == -1))
    before_slic = slice(0, position_begin)
    eq_slic = slice(position_begin, position_end + l)
    after_slic = slice(position_end + l, None)
    if position_begin != -1:
        eq = text[eq_slic]
        text = text[before_slic] + f'XXXXX{count}XX' + text[after_slic]
        return text, eq
    else:
        return None


def convert_equations(text):
    eqs = []
    count = 0
    for pattern_begin, pattern_end in [('\\(', '\\)'), ('\\[', '\\]')]:
        while True:
            result = convert_next(text, pattern_begin, pattern_end, count)
            if result is None:
                break
            else:
                text, eq = result
                eqs.append(eq)
                count += 1
    return text, eqs


tex_begin = r'''
\documentclass[UTF8]{ctexart}
\usepackage{amsmath,amssymb}
\begin{document}
'''
tex_end = r'''
\end{document}
'''

input_path = sys.argv[1]
input_path_base, input_path_ext = os.path.splitext(input_path)
assert input_path_ext != '.tex', "The input file should not end with .tex! Please change to .txt or something else"
output_path = input_path_base + '.tex'
text_original = open(input_path).read()
text_original = connect_paragraphs(text_original)
text_converted, eqs = convert_equations(text_original)
text_converted = text_converted.replace('\\pm', '$\\pm$')
text_converted = split_titles(text_converted)
text_translated = mtranslate.translate(text_converted, language_to, language_from)
text_final = text_translated

for count, eq in enumerate(eqs):
    text_final = text_final.replace(f'XXXXX{count}XX', eq)

with open(output_path, "w") as file:
    print(tex_begin, file=file)
    print(text_final, file=file)
    print(tex_end, file=file)

os.system(f'xelatex {output_path}')
