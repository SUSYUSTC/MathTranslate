#!/usr/bin/env python
import os
import sys

tex_begin = r'''
\documentclass[UTF8]{article}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb}
\begin{document}
'''
tex_end = r'''
\end{document}
'''


language_list = '''
Afrikaans            af
Irish                ga
Albanian             sq
Italian              it
Arabic               ar
Japanese             ja
Azerbaijani          az
Kannada              kn
Basque               eu
Korean               ko
Bengali              bn
Latin                la
Belarusian           be
Latvian              lv
Bulgarian            bg
Lithuanian           lt
Catalan              ca
Macedonian           mk
Chinese_Simplified   zh-CN
Malay                ms
Chinese_Traditional  zh-TW
Maltese              mt
Croatian             hr
Norwegian            no
Czech                cs
Persian              fa
Danish               da
Polish               pl
Dutch                nl
Portuguese           pt
English              en
Romanian             ro
Esperanto            eo
Russian              ru
Estonian             et
Serbian              sr
Filipino             tl
Slovak               sk
Finnish              fi
Slovenian            sl
French               fr
Spanish              es
Galician             gl
Swahili              sw
Georgian             ka
Swedish              sv
German               de
Tamil                ta
Greek                el
Telugu               te
Gujarati             gu
Thai                 th
Haitian_Creole       ht
Turkish              tr
Hebrew               iw
Ukrainian            uk
Hindi                hi
Urdu                 ur
Hungarian            hu
Vietnamese           vi
Icelandic            is
Welsh                cy
Indonesian           id
Yiddish              yi
'''


def variable_code(count):
    return f'XXXXX_{count}_XXXXX'


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
        if line_above[-1] != '.' and (not line_above[0].islower()) and line_below[0].isupper():
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
        text = text[before_slic] + variable_code(count) + text[after_slic]
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


def translate_by_part(Translator, text, language_to, language_from, limit):
    lines = text.split('\n')
    parts = []
    part = ''
    for line in lines:
        if len(part) + len(line) < limit - 10:
            part = part + '\n' + line
        else:
            parts.append(part)
            part = line
    parts.append(part)
    parts_translated = [Translator.translate(part, language_to, language_from) for part in parts]
    text_translated = '\n'.join(parts_translated)
    return text_translated


def translate_tex(input_path, output_path, engine, language_to, language_from):
    if engine == 'google':
        import mtranslate as Translator
    else:
        assert False, 'engine must be google'
    text_original = open(input_path).read()
    text_original = connect_paragraphs(text_original)
    text_converted, eqs = convert_equations(text_original)
    text_converted = text_converted.replace('\\pm', '$\\pm$')
    text_converted = text_converted.replace('Eq.', 'equation')
    text_converted = split_titles(text_converted)
    print(text_converted)
    text_translated = translate_by_part(Translator, text_converted, language_to, language_from, 5000)
    text_final = text_translated

    for count, eq in enumerate(eqs):
        text_final = text_final.replace(variable_code(count), eq)

    with open(output_path, "w") as file:
        print(tex_begin, file=file)
        print(text_final, file=file)
        print(tex_end, file=file)


if __name__ == '__main__':
    from mathtranslate.config import default_engine, default_language_from, default_language_to
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', type=str, help='input file')
    parser.add_argument("-engine", default=default_engine, help=f'translation engine, avaiable options include google. default is {default_engine}')
    parser.add_argument("-from", default=default_language_from, dest='l_from', help=f'language from, default is {default_language_from}')
    parser.add_argument("-to", default=default_language_to, dest='l_to', help=f'language to, default is {default_language_to}')
    parser.add_argument("--list", action='store_true', help='list codes for languages')
    options = parser.parse_args()
    if options.list:
        print(language_list)
        sys.exit()

    if options.file is None:
        parser.print_help()
        sys.exit()

    input_path = options.file
    input_path_base, input_path_ext = os.path.splitext(input_path)
    assert input_path_ext != '.tex', "The input file should not end with .tex! Please change to .txt or something else"
    output_path = input_path_base + '.tex'

    translate_tex(input_path, output_path, options.engine, options.l_to, options.l_from)
    print(output_path, 'is generated')

    os.system(f'xelatex {output_path}')
