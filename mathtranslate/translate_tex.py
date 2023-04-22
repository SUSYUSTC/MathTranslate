#!/usr/bin/env python
import os
import sys
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


def main(args=None):
    from mathtranslate import utils
    from mathtranslate.encoding import get_file_encoding
    from mathtranslate.translate import TextTranslator, LatexTranslator
    utils.check_update()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', type=str, help='input file')
    parser.add_argument("-o", type=str, help='output path')
    utils.add_arguments(parser)
    parser.add_argument("--compile", action='store_true')
    if args is None:
        options = parser.parse_args()
    else:
        options = parser.parse_args(args)

    if options.file is None:
        parser.print_help()
        sys.exit()

    utils.process_options(options)

    print("Start")
    print('engine', options.engine)
    print('language from', options.l_from)
    print('language to', options.l_to)
    input_path = options.file
    if options.o is None:
        input_path_base, input_path_ext = os.path.splitext(input_path)
        if input_path_ext == '.tex':
            print("The input file ends with .tex, it will be overwritten.")
            print("If you confirm this action, please press enter, otherwise ctrl+C to cancel")
            input()
            print('OK I will continue')
        output_path = input_path_base + '.tex'
    else:
        output_path = options.o

    text_translator = TextTranslator(options.engine, options.l_to, options.l_from)
    latex_translator = LatexTranslator(text_translator, options.debug)

    input_encoding = get_file_encoding(input_path)
    text_original = open(input_path, encoding=input_encoding).read()
    text_final = latex_translator.translate_full_latex(text_original)
    with open(output_path, "w", encoding='utf-8') as file:
        print(text_final, file=file)
    print(output_path, 'is generated')

    print('Number of translation called:', text_translator.number_of_calls)
    print('Total characters translated:', text_translator.tot_char)
    if options.compile:
        os.system(f'xelatex {output_path}')
    else:
        print(f"You can then compile it locally by running 'xelatex {output_path}' or compile it online on overleaf")


if __name__ == '__main__':
    main()
