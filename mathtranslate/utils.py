from . import __version__
from .config import config
from .update import get_latest_version
import sys
import re
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

split = lambda s: re.split(r'\s+', s)


def check_update(require_updated=True):
    latest = get_latest_version()
    updated = __version__ == latest
    if updated:
        print("The current mathtranslate is latest")
    else:
        print("The current mathtranslate is not latest, please update by `pip install --upgrade mathtranslate`")
        if (not config.test_environment) and require_updated:
            sys.exit()


def add_arguments(parser):
    parser.add_argument("-engine", default=config.default_engine, help=f'translation engine, avaiable options include google and tencent. default is {config.default_engine}')
    parser.add_argument("-from", default=config.default_language_from, dest='l_from', help=f'language from, default is {config.default_language_from}')
    parser.add_argument("-to", default=config.default_language_to, dest='l_to', help=f'language to, default is {config.default_language_to}')
    parser.add_argument("--list", action='store_true', help='list codes for languages')
    parser.add_argument("--setkey", action='store_true', help='set id and key of tencent translator')
    parser.add_argument("--setdefault", action='store_true', help='set default translation engine and languages')
    parser.add_argument("--threads", default=config.default_threads, type=int, help='threads for tencent translation, default is auto')
    parser.add_argument("--debug", action='store_true', help='Debug options for developers')
    parser.add_argument("--nocache", action='store_true', help='Debug options for developers')
    


def process_options(options):
    if options.setkey:
        print('Tencent secretID')
        config.set_variable(config.tencent_secret_id_path, config.tencent_secret_id_default)
        print('Tencent secretKey')
        config.set_variable(config.tencent_secret_key_path, config.tencent_secret_key_default)
        print('saved!')
        config.load()
        print('secretID:', config.tencent_secret_id)
        print('secretKey:', config.tencent_secret_key)
        sys.exit()

    if options.setdefault:
        print('Translation engine (google or tencent, default google)')
        config.set_variable(config.default_engine_path, config.default_engine_default)
        print('Translation language from (default en)')
        config.set_variable(config.default_language_from_path, config.default_language_from_default)
        print('Translation language to (default zh-CN)')
        config.set_variable(config.default_language_to_path, config.default_language_to_default)
        print('saved!')
        config.load()
        print('engine:', config.default_engine)
        print('language from:', config.default_language_from)
        print('language to:', config.default_language_to)
        sys.exit()

    if options.list:
        print(language_list)
        print('tencent translator does not support some of them')
        sys.exit()

    if options.engine == 'tencent':
        haskey = (config.tencent_secret_id is not None) and (config.tencent_secret_key is not None)
        if not haskey:
            print('Please save ID and key for tencent translation api first by')
            print('translate_tex --setkey')
            sys.exit()
        if options.l_from == 'zh-CN':
            options.l_from = 'zh'
        if options.l_to == 'zh-CN':
            options.l_to = 'zh'

    if options.threads < 0:
        print('threads must be a non-zero integer number (>=0 where 0 means auto)')
        sys.exit()

    print("Start")
    print('engine', options.engine)
    print('language from', options.l_from)
    print('language to', options.l_to)
    
    print('threads', options.threads if options.threads > 0 else 'auto')
    print()
