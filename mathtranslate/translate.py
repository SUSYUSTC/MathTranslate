#!/usr/bin/env python
from . import process_latex
from . import process_text
from .process_text import char_limit

default_begin = r'''
\documentclass[UTF8]{article}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb}
\begin{document}
'''
default_end = r'''
\end{document}
'''


class TextTranslator:
    def __init__(self, engine, language_to, language_from):
        if engine == 'google':
            import mtranslate as translator
        elif engine == 'tencent':
            from mathtranslate.tencent import Translator
            translator = Translator()
        else:
            assert False, "engine must be google or tencent"
        self.translator = translator
        self.language_to = language_to
        self.language_from = language_from

    def translate(self, text):
        return self.translator.translate(text, self.language_to, self.language_from)


class LatexTranslator:
    def __init__(self, translator: TextTranslator, debug=False):
        self.translator = translator
        self.debug = debug
        if self.debug:
            self.f_old = open("text_old", "w", encoding='utf-8')
            self.f_new = open("text_new", "w", encoding='utf-8')
            self.f_env = open("envs", "w", encoding='utf-8')

    def close(self):
        if self.debug:
            self.f_old.close()
            self.f_new.close()
            self.f_env.close()

    def translate_paragraph_text(self, text):
        lines = text.split('\n')
        parts = []
        part = ''
        for line in lines:
            if len(line) >= char_limit:
                assert False, "one line is too long"
            if len(part) + len(line) < char_limit - 10:
                part = part + '\n' + line
            else:
                parts.append(part)
                part = line
        parts.append(part)
        parts_translated = []
        for part in parts:
            parts_translated.append(self.translator.translate(part))
        text_translated = '\n'.join(parts_translated)
        return text_translated.replace("\u200b", "")

    def translate_paragraph_latex(self, latex_original_paragraph, num, complete):
        text_original_paragraph, envs = process_latex.replace_latex_envs(latex_original_paragraph)
        text_original_paragraph = process_text.split_paragraphs(text_original_paragraph)
        if not complete:
            text_original_paragraph = process_text.split_titles(text_original_paragraph)
        text_translated_paragraph = self.translate_paragraph_text(text_original_paragraph)
        if self.debug:
            print(f'\n\nParagraph {num}\n\n', file=self.f_old)
            print(f'\n\nParagraph {num}\n\n', file=self.f_new)
            print(f'\n\nParagraph {num}\n\n', file=self.f_env)
            print(text_original_paragraph, file=self.f_old)
            print(text_translated_paragraph, file=self.f_new)
            for i, env in enumerate(envs):
                print(f'env {i}', file=self.f_env)
                print(env, file=self.f_env)
        latex_translated_paragraph = process_latex.recover_latex_envs(text_translated_paragraph, envs)
        return latex_translated_paragraph

    def translate_latex_env(self, latex_original, env_names, complete, full):
        latex_translated = latex_original

        num = 0

        def process_function(text):
            nonlocal num
            result = self.translate_paragraph_latex(text, num, complete)
            num += 1
            print(num)
            return result

        for env_name in env_names:
            for env_name in [env_name, env_name + '*']:
                if full:
                    begin_code = r'\begin{env_name}'.replace('env_name', env_name)
                    end_code = r'\end{env_name}'.replace('env_name', env_name)
                else:
                    begin_code = r'\env_name{'.replace('env_name', env_name)
                    end_code = r'}'
                latex_translated = process_latex.process_specific_env(latex_translated, begin_code, end_code, process_function)
        return latex_translated

    def translate_full_latex(self, latex_original):
        latex_original = process_latex.remove_tex_comments(latex_original)
        complete = process_latex.is_complete(latex_original)
        if complete:
            print('It is a full latex document')
            latex_original, tex_begin, tex_end = process_latex.split_latex_document(latex_original, r'\begin{document}', r'\end{document}')
            tex_begin = process_latex.remove_blank_lines(tex_begin)
            tex_begin = process_latex.insert_package(tex_begin, 'xeCJK')
        else:
            print('It is not a full latex document')
            latex_original = process_text.connect_paragraphs(latex_original)
            tex_begin = default_begin
            tex_end = default_end

        latex_original_paragraphs = latex_original.split('\n\n')
        latex_translated_paragraphs = []

        num = 0
        print('processing main text')
        for latex_original_paragraph in latex_original_paragraphs:
            latex_translated_paragraph = self.translate_paragraph_latex(latex_original_paragraph, num, complete)
            latex_translated_paragraphs.append(latex_translated_paragraph)
            print(num, '/', len(latex_original_paragraphs))
            num += 1
        latex_translated = '\n\n'.join(latex_translated_paragraphs)

        print('processing latex environments')
        latex_translated = self.translate_latex_env(latex_translated, ['abstract', 'acknowledgments'], complete, True)
        print('processing latex commands')
        latex_translated = self.translate_latex_env(latex_translated, ['section', 'subsection', 'subsubsection', 'subsubsubsection', 'caption', 'subcaption'], complete, False)

        latex_translated = tex_begin + '\n' + latex_translated + '\n' + tex_end

        print('processing title')
        latex_translated = self.translate_latex_env(latex_translated, ['title'], complete, False)
        return latex_translated
