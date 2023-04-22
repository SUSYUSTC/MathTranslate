import mathtranslate.config
from mathtranslate.encoding import get_file_encoding
from mathtranslate.translate import TextTranslator, LatexTranslator


def translate(config):
    if config.engine == 'tencent':
        if config.language_from == 'zh-CN':
            config.language_from = 'zh'
        if config.language_to == 'zh-CN':
            config.language_to = 'zh'

    text_translator = TextTranslator(config.engine, config.language_to, config.language_from)
    latex_translator = LatexTranslator(text_translator, config.debug)

    input_encoding = get_file_encoding(config.file_path)
    text_original = open(config.file_path, encoding=input_encoding).read()
    text_final = latex_translator.translate_full_latex(text_original)
    with open(config.output_path, "w", encoding='utf-8') as file:
        print(text_final, file=file)

