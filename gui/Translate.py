from mathtranslate.config import config
from mathtranslate.encoding import get_file_encoding
from mathtranslate.translate import TextTranslator, LatexTranslator
import sys


def translate(file_path, output_path):
    # redirect standard output to log file
    f = open(config.log_file, 'w', encoding='utf-8')
    sys.stdout = f
    sys.stderr = f

    engine = config.default_engine
    language_from = config.default_language_from
    language_to = config.default_language_to

    print('engine:', engine)
    print('language from:', language_from)
    print('language to:', language_to)
    if engine == 'tencent':
        if language_from == 'zh-CN':
            language_from = 'zh'
        if language_to == 'zh-CN':
            language_to = 'zh'

    text_translator = TextTranslator(engine, language_to, language_from)
    latex_translator = LatexTranslator(text_translator)

    input_encoding = get_file_encoding(file_path)
    text_original = open(file_path, encoding=input_encoding).read()
    text_final = latex_translator.translate_full_latex(text_original)
    with open(output_path, "w", encoding='utf-8') as file:
        print(text_final, file=file)

    print('finished')
    print('file saved to', output_path)

    # restore print
    f.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
