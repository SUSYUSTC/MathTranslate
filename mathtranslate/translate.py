#!/usr/bin/env python
from . import __version__
from . import process_latex
from . import process_text
from . import cache
from .config import config
from .process_latex import environment_list, command_list, format_list
from .process_text import char_limit
from .encoding import get_file_encoding
import time
import re
import tqdm.auto
#import concurrent.futures
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
        self.engine = engine
        if engine == 'google':
            #import mtranslate as translator
            #self.try_translate = lambda text: self.translator.translate(text, self.language_to, self.language_from)
            from mathtranslate.google import ParallelTranslator
            self.translator = ParallelTranslator(language_to, language_from)
            self.try_translate = lambda text: self.translator.translate(text)
            self.combined_char_limit = 5000
        elif engine == 'tencent':
            from mathtranslate.tencent import Translator
            self.translator = Translator()
            self.try_translate = lambda text: self.translator.translate(text, self.language_to, self.language_from)
            self.combined_char_limit = 2000
        else:
            assert False, "engine must be google or tencent"
        self.language_to = language_to
        self.language_from = language_from
        self.number_of_calls = 0
        self.tot_char = 0

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
        self.number_of_calls += 1
        self.tot_char += len(text)
        return result


class LatexTranslator:
    def __init__(self, translator: TextTranslator, debug=False, threads=0):
        self.translator = translator
        self.debug = debug
        if self.debug:
            self.f_old = open("text_old", "w", encoding='utf-8')
            self.f_new = open("text_new", "w", encoding='utf-8')
            self.f_obj = open("objs", "w", encoding='utf-8')
        if threads == 0:
            self.threads = None
        else:
            self.threads = threads
        self.stage = None
        self.record_data = {}

    def close(self):
        if self.debug:
            self.f_old.close()
            self.f_new.close()
            self.f_obj.close()

    def translate_with_record(self, text):
        if self.stage == 'record':
            self.record_data[text] = None
            return text
        elif self.stage == 'load':
            return self.record_data[text]
        elif self.stage == 'translate':
            return self.translator.translate(text)
        else:
            raise ValueError("stage must be 'record', 'load' or 'translate'")

    def split_translation_by_record(self, text, standard):
        words = set(list(standard))
        lines = [[]]
        for line in text.split('\n'):
            this_words = set(list(line))
            if (len(line) < len(words) * 1.5) and (len(line) > len(words) * 0.5) and (len(this_words.intersection(words)) >= len(this_words) * 0.8):
                lines.append([])
            else:
                lines[-1].append(line.strip())
        for i in range(len(lines)):
            lines[i] = '\n'.join(lines[i])
        return lines

    def translate_record_data(self):
        sep = 'This is a translation software.'
        sep_translated = self.translator.translate(sep)
        sep_length = len(sep) + 4
        combined_text_all = []
        texts_to_combine = []
        length_left = self.translator.combined_char_limit
        keys = list(self.record_data.keys())
        for key in keys:
            if length_left < sep_length + len(key):
                combined_text_all.append(f'\n\n{sep}\n\n'.join(texts_to_combine))
                texts_to_combine = [key]
                length_left = self.translator.combined_char_limit - len(key)
            else:
                texts_to_combine.append(key)
                length_left -= sep_length + len(key)
        combined_text_all.append(f'\n\n{sep}\n\n'.join(texts_to_combine))
        translation_results = []
        for item in tqdm.tqdm(combined_text_all):
            result = self.translator.translate(item)
            results = self.split_translation_by_record(result, sep_translated)
            if len(results) != len(item.split(sep)):
                raise ValueError()
            translation_results += results
        assert len(translation_results) == len(keys)
        self.record_data = dict(zip(keys, translation_results))

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
            text_original = part.strip()
            if text_original.upper() == text_original:
                result = text_original
            else:
                result = self.translate_with_record(part)
                #result = self.translator.translate(part)
            parts_translated.append(result)
        text_translated = '\n'.join(parts_translated)
        return text_translated.replace("\u200b", "")

    def replace_with_uppercase(self, text, word):
        # Construct a regex pattern that matches the word regardless of case
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        # Replace all matches with the uppercase version of the word
        result = pattern.sub(word.upper(), text)
        return result

    def _translate_text_in_paragraph_latex(self, latex_original_paragraph):
        '''
        Translate a latex paragraph, which means that it could contain latex objects
        '''

        # remove format about textbf, emph and textit
        for format_name in format_list:
            latex_original_paragraph = process_latex.delete_specific_format(latex_original_paragraph, format_name)

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
        text_translated_paragraph = self.replace_with_uppercase(text_translated_paragraph, config.math_code)
        if self.debug:
            print(f'\n\nParagraph {self.num}\n\n', file=self.f_new)
            print(text_translated_paragraph, file=self.f_new)
            print(f'\n\nParagraph {self.num}\n\n', file=self.f_obj)
            for i, obj in enumerate(objs):
                print(f'obj {i}', file=self.f_obj)
                print(obj, file=self.f_obj)
        latex_translated_paragraph, nbad, ntotal = process_latex.recover_latex_objects(text_translated_paragraph, objs, tolerate_error=True)
        self.nbad += nbad
        self.ntotal += ntotal
        return latex_translated_paragraph

    def translate_text_in_paragraph_latex(self, paragraph):
        splited_paragraphs, seps = process_latex.split_by_command(paragraph)
        result = ''
        for split, sep in zip(splited_paragraphs, seps):
            result += self._translate_text_in_paragraph_latex(split) + ' ' + sep + ' '
        return result

    def translate_latex_all_objects(self, latex):
        '''
        Terminology:
        env: '\\begin{xxx} \\end{xxx}'
        command: '\\command[options]{text}
        object: env or command
        '''
        translate_function = self.translate_text_in_paragraph_latex_and_leading_brace
        for env_name in environment_list + self.theorems:
            latex = process_latex.process_specific_env(latex, translate_function, env_name)
            latex = process_latex.process_specific_env(latex, translate_function, env_name + r'\*')
        for command_name in command_list:
            latex = process_latex.process_specific_command(latex, translate_function, command_name)
            latex = process_latex.process_specific_command(latex, translate_function, command_name + r'\*')
        for command_group in config.mularg_command_list:
            latex = process_latex.process_mularg_command(latex, translate_function, command_group)
        return latex

    def translate_text_in_paragraph_latex_and_leading_brace(self, latex_original_paragraph):
        # it acts recursively, i.e. it also translates braces inside braces
        latex_translated_paragraph = self.translate_text_in_paragraph_latex(latex_original_paragraph)
        latex_translated_paragraph = process_latex.process_leading_level_brace(latex_translated_paragraph, self.translate_text_in_paragraph_latex_and_leading_brace)
        return latex_translated_paragraph

    def translate_paragraph_latex(self, latex_original_paragraph):
        latex_translated_paragraph = self.translate_text_in_paragraph_latex_and_leading_brace(latex_original_paragraph)
        latex_translated_paragraph = self.translate_latex_all_objects(latex_translated_paragraph)
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

    def worker(self, latex_original_paragraph):
        try:
            if self.add_cache:
                hash_key_paragraph = cache.deterministic_hash(latex_original_paragraph)
                latex_translated_paragraph = cache.load_paragraph(self.hash_key, hash_key_paragraph)
                if latex_translated_paragraph is None:
                    latex_translated_paragraph = self.translate_paragraph_latex(latex_original_paragraph)
                    cache.write_paragraph(self.hash_key, hash_key_paragraph, latex_translated_paragraph)
            else:
                latex_translated_paragraph = self.translate_paragraph_latex(latex_original_paragraph)
            self.num += 1
            return latex_translated_paragraph
        except BaseException as e:
            print('Error found in Parapragh', self.num)
            print('Content')
            print(latex_original_paragraph)
            raise e

    def translate_full_latex(self, latex_original, make_complete=True, nocache=False):
        self.add_cache = (not nocache)
        if self.add_cache:
            cache.remove_extra()
            self.hash_key = cache.deterministic_hash((latex_original, __version__, self.translator.engine, self.translator.language_from, self.translator.language_to, config.mularg_command_list))
            if cache.is_cached(self.hash_key):
                print('Cache is found')
            cache.create_cache(self.hash_key)

        self.nbad = 0
        self.ntotal = 0

        latex_original = process_latex.remove_tex_comments(latex_original)
        latex_original = latex_original.replace(r'\mathbf', r'\boldsymbol')
        # \bibinfo {note} is not working in xelatex
        latex_original = process_latex.remove_bibnote(latex_original)
        latex_original = process_latex.process_newcommands(latex_original)

        latex_original = process_latex.replace_accent(latex_original)
        latex_original = process_latex.replace_special(latex_original)

        self.complete = process_latex.is_complete(latex_original)
        self.theorems = process_latex.get_theorems(latex_original)
        if self.complete:
            print('It is a full latex document')
            latex_original, tex_begin, tex_end = process_latex.split_latex_document(latex_original, r'\begin{document}', r'\end{document}')
            tex_begin = process_latex.remove_blank_lines(tex_begin)
            tex_begin = process_latex.insert_macro(tex_begin, '\\usepackage{xeCJK}\n\\usepackage{amsmath}')
        else:
            print('It is not a full latex document')
            latex_original = process_text.connect_paragraphs(latex_original)
            if make_complete:
                tex_begin = default_begin
                tex_end = default_end
            else:
                tex_begin = ''
                tex_end = ''

        latex_original_paragraphs = self.split_latex_to_paragraphs(latex_original)
        latex_translated_paragraphs = []
        self.num = 0
        # tqdm with concurrent.futures.ThreadPoolExecutor()

        self.stage = 'record'
        for latex_original_paragraph in latex_original_paragraphs:
            self.translate_paragraph_latex(latex_original_paragraph)

        #with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
        #    values = list(executor.map(self.translator.translate, self.record_data.keys()))
        #    #latex_translated_paragraphs = list(tqdm.auto.tqdm(executor.map(self.worker, latex_original_paragraphs), total=len(latex_original_paragraphs)))
        #self.record_data = dict(zip(self.record_data.keys(), values))
        self.translate_record_data()

        self.stage = 'load'
        latex_translated_paragraphs = [self.translate_paragraph_latex(latex_original_paragraph) for latex_original_paragraph in latex_original_paragraphs]

        latex_translated = '\n\n'.join(latex_translated_paragraphs)

        latex_translated = tex_begin + '\n' + latex_translated + '\n' + tex_end

        # Title is probably outside the body part
        self.num = 'title'
        self.stage = 'translate'
        latex_translated = process_latex.process_specific_command(latex_translated, self.translate_text_in_paragraph_latex, 'title')

        latex_translated = latex_translated.replace('%', '\\%')
        latex_translated = process_latex.recover_special(latex_translated)
        latex_translated = process_latex.recover_accent(latex_translated)

        self.close()

        print(self.ntotal - self.nbad, '/',  self.ntotal, 'latex object are correctly translated')

        return latex_translated


def translate_single_tex_file(input_path, output_path, engine, l_from, l_to, debug, nocache, threads):
    text_translator = TextTranslator(engine, l_to, l_from)
    latex_translator = LatexTranslator(text_translator, debug, threads)

    input_encoding = get_file_encoding(input_path)
    text_original = open(input_path, encoding=input_encoding).read()
    text_final = latex_translator.translate_full_latex(text_original, nocache=nocache)
    with open(output_path, "w", encoding='utf-8') as file:
        print(text_final, file=file)
    print('Number of translation called:', text_translator.number_of_calls)
    print('Total characters translated:', text_translator.tot_char)
    print('saved to', output_path)
