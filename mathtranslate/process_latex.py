import re
from .config import math_code

match_code = r"(" + math_code + r"_\d+(?:_\d+)*)"


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
    # define regular expressions for each LaTeX environment
    latex_env_regex = [
        r"(?<!\\)\\\[(.*?)(?<!\\)\\\]",  # \[ xxx \]
        r"(?<!\\)\\begin\{(.*?)\}(.*?)(?<!\\)\\end\{\1\}",  # \begin{xxx} \end{xxx}
        r"(?<!\\)\$\$(.*?)(?<!\\)\$\$",  # $$ $$
        r"(?<!\\)\$(.*?)(?<!\\)\$",  # $ $
        r"(?<!\\)\\\((.*?)(?<!\\)\\\)",  # \( xxx \)
        r"(?<!\\)\\([a-zA-Z]+)\[(.*?)\]\{(.*?)\}",  # \xxx[xxx]{xxx}
        r"(?<!\\)\\([a-zA-Z]+)\{(.*?)\}",  # \xxx{xxx}
        r"(?<!\\)\\([a-zA-Z]+)",  # \xxx
    ]

    # iterate through each LaTeX environment and replace with "XMATH_{digit1}_{digit2}_..._{digit_last}"
    count = 0
    replaced_envs = []
    for regex in latex_env_regex:
        pattern = re.compile(regex, re.DOTALL)
        while pattern.search(text):
            latex_env = pattern.search(text).group()
            replaced_envs.append(latex_env)
            text = pattern.sub(variable_code(count), text, 1)
            count += 1

    text = modify_text(text, modify_before)
    return text, replaced_envs


def recover_latex_envs(text, replaced_envs):
    text = modify_text(text, modify_after)
    for count, env in list(enumerate(replaced_envs))[::-1]:
        text = text.replace(variable_code(count), env)
    return text
