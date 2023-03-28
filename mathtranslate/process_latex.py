import re
import regex
from .config import math_code

match_code = r"(" + math_code + r"_\d+(?:_\d+)*)"
match_code_replace = math_code + r"_(\d+(?:_\d+)*)*"
pattern_env = r"\\begin\{(.*?)\}(.*?)\\end\{\1\}"  # \begin{xxx} \end{xxx}, group 1: name, group 2: content
pattern_command_full = r"\\([a-zA-Z]+\*?)?(\[[a-zA-Z\s,]*?\])?(\{((?:[^{}]++|(?3))++)\})"   # \xxx[xxx]{xxx} and \xxx{xxx}, group 1: name, group 2: option, group 4: content
pattern_command_simple = r"\\([a-zA-Z]+)"  # \xxx, group 1: name


def variable_code(count):
    digits = list(str(count))
    count_str = "_".join(digits)
    return f'{math_code}_{count_str}'


def modify_text(text, modify_func):
    split_text = [s for s in re.split(match_code, text) if s is not None]
    for i in range(len(split_text)):
        if not re.match(match_code, split_text[i]):
            split_text[i] = modify_func(split_text[i])
    text = "".join(split_text)
    return text


def modify_before(text):
    text = text.replace('\\pm', '$\\pm$')
    text = text.replace('Eq.', 'equation')
    return text


def modify_after(text):
    pattern = r"(?<!\\)_"
    text = re.sub(pattern, r"\\_", text)
    return text


def replace_latex_envs(text):
    r"""
    Replaces all LaTeX environments in a given text with the format "XMATH_{digit1}_{digit2}_..._{digit_last}",
    applies a given function to the resulting text (excluding the "XMATH_{digit1}_{digit2}_..._{digit_last}" parts),
    and returns both the processed text and a list of replaced LaTeX environments.
    Supported LaTeX environments: \[ xxx \], \begin{xxx} \end{xxx}, $$ $$,
    $ $, \( xxx \), \xxx[xxx]{xxx}, \xxx{xxx}, and \xxx.
    Returns the processed text and a list of replaced LaTeX environments.
    """
    # TODO: for \xxx[xxx]{xxx} and \xxx{xxx} the regex here cannot process \xxx{xxx{xxx}} correctly.
    # We need to either change the regex or use the function "process_specific_env" in the following.
    # Here is a regex that works better but cannot process \xxx{xxx \{xxx\}}: r'(?<!\\)\\[a-zA-Z]+?(\{(?:[^{}]++|(?1))++\})'

    # define regular expressions for each LaTeX environment
    latex_env_regex = [
        r"\$\$(.*?)\$\$",  # $$ $$
        r"\$(.*?)\$",  # $ $
        r"\\\[(.*?)\\\]",  # \[ xxx \]
        r"\\\((.*?)\\\)",  # \( xxx \)
        pattern_env,  # \begin{xxx} \end{xxx}
        pattern_command_full,  # \xxx[xxx]{xxx}
        pattern_command_simple,  # \xxx
    ]

    # iterate through each LaTeX environment and replace with "XMATH_{digit1}_{digit2}_..._{digit_last}"
    count = 0
    replaced_envs = []
    for regex_symbol in latex_env_regex:
        pattern = regex.compile(regex_symbol, regex.DOTALL)
        while pattern.search(text):
            latex_env = pattern.search(text).group()
            replaced_envs.append(f' {latex_env} ')
            text = pattern.sub(variable_code(count), text, 1)
            count += 1

    text = modify_text(text, modify_before)
    return text, replaced_envs


def recover_latex_envs(text, replaced_envs, verbose=False):
    nenvs = len(replaced_envs)
    matched_indices = []

    def get_env(digit_str):
        index = int(''.join(digit_str.split('_')))
        matched_indices.append(index)
        if index < nenvs:
            return replaced_envs[index]
        else:
            return '???'

    text = modify_text(text, modify_after)
    pattern = re.compile(match_code_replace)
    total_num = 0
    while True:
        text, num_modify = pattern.subn(lambda match: get_env(match.group(1)), text)
        total_num += num_modify
        if num_modify == 0:
            break
    n_good = len(set(matched_indices).intersection(set(range(nenvs))))
    n_bad1 = len(matched_indices) - n_good
    n_bad2 = nenvs - n_good
    n_bad = max(n_bad1, n_bad2)
    if verbose and n_bad > 0:
        print(n_bad, 'latex environments are wrong in total', nenvs)
    return text


def remove_tex_comments(text):
    """
    Removes all TeX comments in a given string with the format "% comment text".
    Does not match "\%".
    Returns the processed string.
    """
    text = re.sub(r"\n(?<!\\)%.*?(?=\n)", "", text)
    text = re.sub(r"(?<!\\)%.*?(?=\n)", "", text)

    return text


def split_latex_document(text, begin_code, end_code):
    """
    Splits a document into three parts: the preamble, the body, and the postamble.
    Returns a tuple of the three parts.
    """
    begin_doc_index = text.find(begin_code)
    end_doc_index = text.rfind(end_code)
    if begin_doc_index == -1 or end_doc_index == -1 or end_doc_index <= begin_doc_index:
        assert False, "latex is not complete"
    pre = text[:begin_doc_index + len(begin_code)]
    body = text[begin_doc_index + len(begin_code):end_doc_index]
    post = text[end_doc_index:]
    return body, pre, post


def count_braces(text):
    text = text.replace(r'\{', '')
    text = text.replace(r'\}', '')
    return text.count('{'), text.count('}')


def process_specific_env(latex, function, env_names):
    pattern = regex.compile(pattern_env, regex.DOTALL)

    def process_function(match):
        env_name = match.group(1)
        content = match.group(2)
        if env_name in env_names:
            processed_content = function(content)
            return rf'\begin{{{env_name}}}{processed_content}\end{{{env_name}}}'
        else:
            return match.group(0)
    return pattern.sub(process_function, latex)


def process_specific_commands(latex, function, command_names):
    pattern = regex.compile(pattern_command_full, regex.DOTALL)

    def process_function(match):
        command_name = match.group(1)
        options = match.group(2)
        if options is None:
            options = ''
        content = match.group(4)
        if command_name in command_names:
            processed_content = function(content)
            return rf'\{command_name}{options}{{{processed_content}}}'
        else:
            return match.group(0)
    return pattern.sub(process_function, latex)


def old_process_specific_env(text, pattern_begin, pattern_end, function):
    position = 0
    while True:
        position = text.find(pattern_begin, position)
        if position == -1:
            break
        position += len(pattern_begin)
        start = position
        while True:
            position = text.find(pattern_end, position)
            if position > 0 and text[position - 1] != '\\':
                n_left, n_right = count_braces(text[start:position])
                if n_left == n_right:
                    break
            position += 1
        text_before = text[0:start]
        text_middle = function(text[start:position])
        text_after = text[position:]
        position = len(text_before) + len(text_middle) + len(pattern_end)
        text = text_before + text_middle + text_after
    return text


def remove_blank_lines(text):
    pattern = re.compile(r'\n\n+')
    text = pattern.sub('\n', text)
    return text


def insert_package(text, package):
    pattern = re.compile(r"\\documentclass(\[.*?\])?\{(.*?)\}", re.DOTALL)
    match = pattern.search(text)
    if match:
        start, end = match.span()
        new_text = text[:end] + f"\n\\usepackage{{{package}}}\n" + text[end:]
        return new_text
    else:
        return text


def is_complete(latex_code):
    # Define regular expressions for \documentclass, \begin{document}, and \end{document}
    documentclass_pattern = re.compile(r"\\documentclass(\[.*?\])?\{.*?\}", re.DOTALL)
    begin_pattern = re.compile(r"\\begin\{document\}")
    end_pattern = re.compile(r"\\end\{document\}")

    # Check if \documentclass is present
    if not documentclass_pattern.search(latex_code):
        return False

    # Check if \begin{document} is present
    begin_match = begin_pattern.search(latex_code)
    if not begin_match:
        return False
    begin_index = begin_match.start()

    # Check if \end{document} is present
    end_match = end_pattern.search(latex_code)
    if not end_match:
        return False
    end_index = end_match.end()

    # Check if the order is correct
    if begin_index < documentclass_pattern.search(latex_code).end() or end_index < begin_index:
        return False

    return True
