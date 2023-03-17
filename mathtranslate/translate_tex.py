#!/usr/bin/env python
import os
import sys
import mtranslate

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
┌───────────────────────┬───────────────────────┬───────────────────────┐
│ Afrikaans      -   af │ Hebrew         -   he │ Portuguese     -   pt │
│ Albanian       -   sq │ Hill Mari      -  mrj │ Punjabi        -   pa │
│ Amharic        -   am │ Hindi          -   hi │ Querétaro Otomi-  otq │
│ Arabic         -   ar │ Hmong          -  hmn │ Romanian       -   ro │
│ Armenian       -   hy │ Hmong Daw      -  mww │ Russian        -   ru │
│ Azerbaijani    -   az │ Hungarian      -   hu │ Samoan         -   sm │
│ Bashkir        -   ba │ Icelandic      -   is │ Scots Gaelic   -   gd │
│ Basque         -   eu │ Igbo           -   ig │ Serbian (Cyr...-sr-Cyrl
│ Belarusian     -   be │ Indonesian     -   id │ Serbian (Latin)-sr-Latn
│ Bengali        -   bn │ Irish          -   ga │ Sesotho        -   st │
│ Bosnian        -   bs │ Italian        -   it │ Shona          -   sn │
│ Bulgarian      -   bg │ Japanese       -   ja │ Sindhi         -   sd │
│ Cantonese      -  yue │ Javanese       -   jv │ Sinhala        -   si │
│ Catalan        -   ca │ Kannada        -   kn │ Slovak         -   sk │
│ Cebuano        -  ceb │ Kazakh         -   kk │ Slovenian      -   sl │
│ Chichewa       -   ny │ Khmer          -   km │ Somali         -   so │
│ Chinese Simp...- zh-CN│ Klingon        -  tlh │ Spanish        -   es │
│ Chinese Trad...- zh-TW│ Klingon (pIqaD)tlh-Qaak Sundanese      -   su │
│ Corsican       -   co │ Korean         -   ko │ Swahili        -   sw │
│ Croatian       -   hr │ Kurdish        -   ku │ Swedish        -   sv │
│ Czech          -   cs │ Kyrgyz         -   ky │ Tahitian       -   ty │
│ Danish         -   da │ Lao            -   lo │ Tajik          -   tg │
│ Dutch          -   nl │ Latin          -   la │ Tamil          -   ta │
│ Eastern Mari   -  mhr │ Latvian        -   lv │ Tatar          -   tt │
│ Emoji          -  emj │ Lithuanian     -   lt │ Telugu         -   te │
│ English        -   en │ Luxembourgish  -   lb │ Thai           -   th │
│ Esperanto      -   eo │ Macedonian     -   mk │ Tongan         -   to │
│ Estonian       -   et │ Malagasy       -   mg │ Turkish        -   tr │
│ Fijian         -   fj │ Malay          -   ms │ Udmurt         -  udm │
│ Filipino       -   tl │ Malayalam      -   ml │ Ukrainian      -   uk │
│ Finnish        -   fi │ Maltese        -   mt │ Urdu           -   ur │
│ French         -   fr │ Maori          -   mi │ Uzbek          -   uz │
│ Frisian        -   fy │ Marathi        -   mr │ Vietnamese     -   vi │
│ Galician       -   gl │ Mongolian      -   mn │ Welsh          -   cy │
│ Georgian       -   ka │ Myanmar        -   my │ Xhosa          -   xh │
│ German         -   de │ Nepali         -   ne │ Yiddish        -   yi │
│ Greek          -   el │ Norwegian      -   no │ Yoruba         -   yo │
│ Gujarati       -   gu │ Papiamento     -  pap │ Yucatec Maya   -  yua │
│ Haitian Creole -   ht │ Pashto         -   ps │ Zulu           -   zu │
│ Hausa          -   ha │ Persian        -   fa │                       │
│ Hawaiian       -  haw │ Polish         -   pl │                       │
└───────────────────────┴───────────────────────┴───────────────────────┘
'''


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


def translate_tex(input_path, output_path, language_to, language_from):
    text_original = open(input_path).read()
    text_original = connect_paragraphs(text_original)
    text_converted, eqs = convert_equations(text_original)
    text_converted = text_converted.replace('\\pm', '$\\pm$')
    text_converted = text_converted.replace('Eq.', 'equation')
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


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs=1, type=str, description='input file')
    parser.add_argument("-from", default='en', dest='l_from', description='language from')
    parser.add_argument("-to", default='zh-CN', dest='l_to', description='language to')
    parser.add_argument("--list", action='store_true', description='list all languages')
    options = parser.parse_args()
    if options.l:
        print(language_list)
        sys.exit()

    input_path = options.file
    input_path_base, input_path_ext = os.path.splitext(input_path)
    assert input_path_ext != '.tex', "The input file should not end with .tex! Please change to .txt or something else"
    output_path = input_path_base + '.tex'

    translate_tex(input_path, output_path, options.l_to, options.l_from)
