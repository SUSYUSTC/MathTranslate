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


def main():
    import mathtranslate
    from mathtranslate import config
    from mathtranslate.config import default_engine, default_language_from, default_language_to
    from mathtranslate.fix_encoding import fix_file_encoding
    from mathtranslate.translate import TextTranslator, LatexTranslator
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', type=str, help='input file')
    parser.add_argument("-o", type=str, help='output path')
    parser.add_argument("-engine", default=default_engine, help=f'translation engine, avaiable options include google and tencent. default is {default_engine}')
    parser.add_argument("-from", default=default_language_from, dest='l_from', help=f'language from, default is {default_language_from}')
    parser.add_argument("-to", default=default_language_to, dest='l_to', help=f'language to, default is {default_language_to}')
    parser.add_argument("--list", action='store_true', help='list codes for languages')
    parser.add_argument("--setkey", action='store_true', help='set id and key of tencent translator')
    parser.add_argument("--setdefault", action='store_true', help='set default translation engine and languages')
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--compile", action='store_true')
    options = parser.parse_args()

    if options.setkey:
        print('Tencent API ID')
        config.set_variable(config.tencent_secret_id_path, config.tencent_secret_id_default)
        print('Tencent API Key')
        config.set_variable(config.tencent_secret_key_path, config.tencent_secret_key_default)
        print('saved!')
        config.reread()
        print('ID:', config.tencent_secret_id)
        print('Key:', config.tencent_secret_key)
        sys.exit()

    if options.setdefault:
        print('Translation engine (default google)')
        config.set_variable(config.default_engine_path, config.default_engine_default)
        print('Translation language from (default en)')
        config.set_variable(config.default_language_from_path, config.default_language_from_default)
        print('Translation language to (default zh-CN)')
        config.set_variable(config.default_language_to_path, config.default_language_to_default)
        print('saved!')
        config.reread()
        print('engine:', config.default_engine)
        print('language from:', config.default_language_from)
        print('language to:', config.default_language_to)
        sys.exit()

    if options.list:
        print(language_list)
        print('tencent translator does not support some of them')
        sys.exit()

    if options.file is None:
        parser.print_help()
        sys.exit()

    if options.engine == 'tencent':
        haskey = (mathtranslate.config.tencent_secret_id is not None) and (mathtranslate.config.tencent_secret_key is not None)
        if not haskey:
            print('Please save ID and key for tencent translation api first by')
            print('translate_tex --setkey')
            sys.exit()
        if options.l_from == 'zh-CN':
            options.l_from = 'zh'
        if options.l_to == 'zh-CN':
            options.l_to = 'zh'

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

    text_original = open(input_path).read()
    text_final = latex_translator.translate_full_latex(text_original)
    with open(output_path, "w", encoding='utf-8') as file:
        print(text_final, file=file)
    print(output_path, 'is generated')
    fix_file_encoding(output_path)

    if options.compile:
        os.system(f'xelatex {output_path}')
    else:
        print(f"You can then manually compile it by running 'xelatex {output_path}'")
        print("or compile it online on overleaf")


if __name__ == '__main__':
    main()
