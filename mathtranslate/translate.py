#!/usr/bin/env python
from . import process_latex
from . import process_text
from .process_text import char_limit
import time
import re
import tqdm

default_begin = r'''
\documentclass[UTF8]{article}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb}
\begin{document}
'''
default_end = r'''
\end{document}
'''

# TODO: add more here
environment_list = ['abstract', 'acknowledgments', 'itemize', 'enumerate', 'description', 'list', 'proof']
command_list = ['section', 'subsection', 'subsubsection', 'caption', 'subcaption', 'footnote', 'paragraph']


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

    def try_translate(self, text):
        return self.translator.translate(text, self.language_to, self.language_from)

    def translate(self, text):
        if not re.match(re.compile(r'.*[a-zA-Z].*', re.DOTALL), text):
            # no meaningful word inside
            return text
        while True:
            try:
                result = self.try_translate(text)
                break
            except BaseException as e:
                if hasattr(self.translator, "is_error_request_frequency") and self.translator.is_error_request_frequency(e):
                    time.sleep(0.5)
                else:
                    raise e
        return result


class LatexTranslator:
    def __init__(self, translator: TextTranslator, debug=False):
        self.translator = translator
        self.debug = debug
        if self.debug:
            self.f_old = open("text_old", "w", encoding='utf-8')
            self.f_new = open("text_new", "w", encoding='utf-8')
            self.f_obj = open("objs", "w", encoding='utf-8')

    def close(self):
        if self.debug:
            self.f_old.close()
            self.f_new.close()
            self.f_obj.close()

    def translate_paragraph_text(self, text):
        '''
        Translators would have a word limit for each translation
        So here we split translation by '\n' if it's going to exceed limit
        '''
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

    def translate_paragraph_latex(self, latex_original_paragraph):
        '''
        Translate a latex paragraph, which means that it could contain latex objects
        '''
        text_original_paragraph, objs = process_latex.replace_latex_objects(latex_original_paragraph)
        # Since \n is equivalent to space in latex, we change \n back to space
        # otherwise the translators view them as separate sentences
        text_original_paragraph = process_latex.combine_split_to_sentences(text_original_paragraph)
        text_original_paragraph = process_text.split_too_long_paragraphs(text_original_paragraph)
        if not self.complete:
            text_original_paragraph = process_text.split_titles(text_original_paragraph)
        # Remove additional space
        text_original_paragraph = re.sub(r'  +', ' ', text_original_paragraph)
        if self.debug:
            print(f'\n\nParagraph {self.num}\n\n', file=self.f_old)
            print(text_original_paragraph, file=self.f_old)
        text_translated_paragraph = self.translate_paragraph_text(text_original_paragraph)
        if self.debug:
            print(f'\n\nParagraph {self.num}\n\n', file=self.f_new)
            print(text_translated_paragraph, file=self.f_new)
            print(f'\n\nParagraph {self.num}\n\n', file=self.f_obj)
            for i, obj in enumerate(objs):
                print(f'obj {i}', file=self.f_obj)
                print(obj, file=self.f_obj)
        latex_translated_paragraph, nbad, ntotal = process_latex.recover_latex_objects(text_translated_paragraph, objs, final=True)
        self.nbad += nbad
        self.ntotal += ntotal
        return latex_translated_paragraph

    def split_latex_to_paragraphs(self, latex):
        '''
        1. convert latex to text and objects
        2. split text
        3. convert text back to objects
        '''
        text, objs = process_latex.replace_latex_objects(latex)
        paragraphs_text = re.split(r'\n\n+', text)
        paragraphs_latex = [process_latex.recover_latex_objects(paragraph_text, objs)[0] for paragraph_text in paragraphs_text]
        return paragraphs_latex

    def translate_latex_all_objects(self, latex, envs, commands):
        '''
        Terminology:
        env: '\\begin{xxx} \\end{xxx}'
        command: '\\command[options]{text}
        object: env or command
        '''
        for env_name in envs:
            latex = process_latex.process_specific_env(latex, self.translate_paragraph_latex, env_name)
            latex = process_latex.process_specific_env(latex, self.translate_paragraph_latex, env_name + r'\*')
        for command_name in commands:
            latex = process_latex.process_specific_command(latex, self.translate_paragraph_latex, command_name)
            latex = process_latex.process_specific_command(latex, self.translate_paragraph_latex, command_name + r'\*')
        return latex

    def translate_full_latex(self, latex_original):
        self.nbad = 0
        self.ntotal = 0

        latex_original = process_latex.remove_tex_comments(latex_original)

        latex_original = process_latex.replace_accent(latex_original)
        latex_original = process_latex.replace_special(latex_original)

        self.complete = process_latex.is_complete(latex_original)
        theorems = process_latex.get_theorems(latex_original)
        if self.complete:
            print('It is a full latex document')
            latex_original, tex_begin, tex_end = process_latex.split_latex_document(latex_original, r'\begin{document}', r'\end{document}')
            tex_begin = process_latex.remove_blank_lines(tex_begin)
            # TODO: change xeCJK to be compatible with other compiler & languages
            tex_begin = process_latex.insert_macro(tex_begin, r'\usepackage{xeCJK}')
        else:
            print('It is not a full latex document')
            latex_original = process_text.connect_paragraphs(latex_original)
            tex_begin = default_begin
            tex_end = default_end

        latex_original_paragraphs = self.split_latex_to_paragraphs(latex_original)
        latex_translated_paragraphs = []

        self.num = 0
        for latex_original_paragraph in tqdm.tqdm(latex_original_paragraphs):
            try:
                latex_translated_paragraph = self.translate_paragraph_latex(latex_original_paragraph)
                latex_translated_paragraph = self.translate_latex_all_objects(latex_translated_paragraph, environment_list + theorems, command_list)
                latex_translated_paragraphs.append(latex_translated_paragraph)
            except BaseException as e:
                print('Error found in Parapragh', self.num)
                print('Content')
                print(latex_original_paragraph)
                raise e
            self.num += 1

        latex_translated = '\n\n'.join(latex_translated_paragraphs)

        latex_translated = tex_begin + '\n' + latex_translated + '\n' + tex_end

        # Title is probably outside the body part
        self.num = 'title'
        latex_translated = process_latex.process_specific_command(latex_translated, self.translate_paragraph_latex, 'title')

        latex_translated = process_latex.recover_special(latex_translated)
        latex_translated = process_latex.recover_accent(latex_translated)

        self.close()

        print(self.ntotal - self.nbad, '/',  self.ntotal, 'latex object are correctly translated')

        return latex_translated
