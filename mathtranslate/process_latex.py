import re
import regex
from .config import config

math_code = config.math_code
test_environment = config.test_environment

match_code = r"(" + math_code + r"_\d+(?:_\d+)*)"
match_code_replace = math_code + r"_(\d+(?:_\d+)*)*"

#options = r"\[[a-zA-Z\s,\\\*\.\+\-=_{}\(\)\!]*?\]"  # ,\*.+-=_{}!
options = r"\[[^\[\]]*?\]"
spaces = r"[ \t]*"

get_pattern_brace = lambda index: rf"\{{((?:[^{{}}]++|(?{index}))*+)\}}"
get_pattern_env = lambda name: rf"\\begin{spaces}\{{({name})\}}{spaces}({options})?(.*?)\\end{spaces}\{{\1\}}"


def get_pattern_command_full(name, n=None):
    pattern = rf'\\({name})'
    if n is None:
        pattern += rf'{spaces}({options})?'
        n = 1
        begin_brace = 3
    else:
        begin_brace = 2
    for i in range(n):
        tmp = get_pattern_brace(i*2+begin_brace)
        pattern += rf'{spaces}({tmp})'
    if n == 0:
        pattern += r'(?=[^a-zA-Z])'
    return pattern


match_command_name = r'[a-zA-Z]+\*?'

pattern_env = get_pattern_env(r'.*?')  # \begin{xxx} \end{xxx}, group 1: name, group 2: option, group 3: content
pattern_command_full = get_pattern_command_full(match_command_name)   # \xxx[xxx]{xxx} and \xxx{xxx}, group 1: name, group 2: option, group 4: content
pattern_command_simple = rf'\\({match_command_name})'  # \xxx, group 1: name
pattern_brace = get_pattern_brace(0)  # {xxx}, group 1: content
pattern_newcommand = rf'\\(?:newcommand|def){spaces}(?:\{{\\([a-zA-Z]+)\}}|\\([a-zA-Z]+)){spaces}(?:\[(\d)\])?{spaces}({get_pattern_brace(4)})'  # \newcommand{name}[n_arguments]{content}, group 1/2: name, group 3: n_arguments, group 5: content

pattern_set1 = rf'\\set[a-zA-Z]*{spaces}\\[a-zA-Z]+{spaces}\{{.*?\}}'
pattern_set2 = rf'\\set[a-zA-Z]*{spaces}\{{\\[a-zA-Z]+\}}{spaces}\{{.*?\}}'
pattern_theorem = r"\\newtheorem[ \t]*\{(.+?)\}"  # \newtheorem{xxx}, group 1: name
pattern_accent = r"\\([`'\"^~=.])(?:\{([a-zA-Z])\}|([a-zA-Z]))"  # match special characters with accents, group 1: accent, group 2/3: normal character
match_code_accent = rf'{math_code}([A-Z]{{2}})([a-zA-Z])'  # group 1: accent name, group 2: normal character, e.g. \"o or \"{o}
list_special = ['\\', '%', '&', '#', '$', '{', '}', ' ']  # all special characters in form of \x

special_character_forward = {
    '\\': 'BS',
    '%': 'PC',
    '&': 'AD',
    '#': 'NB',
    '$': 'DL',
    '{': 'LB',
    '}': 'RB',
    '^': 'UT',
    ' ': 'SP',
    '`': 'BQ',
    '~': 'TD',
    "'": 'SQ',
    '"': 'DQ',
    '=': 'EQ',
    '.': 'DT',
    '*': 'ST',
    '@': 'AT',
}
special_character_backward = {special_character_forward[key]: key for key in special_character_forward}
assert len(set(special_character_forward.values())) == len(special_character_forward)

environment_list = ['abstract', 'acknowledgments', 'itemize', 'enumerate', 'description', 'list', 'proof', 'quote', 'spacing']
command_list = ['section', 'subsection', 'subsubsection', 'caption', 'subcaption', 'footnote', 'paragraph']
format_list = ['textbf', 'textit', 'emph']
replace_newcommand_list = ['equation', 'array', 'displaymath', 'align', 'multiple', 'gather', 'theorem', 'textcolor'] + environment_list + command_list


def variable_code(count):
    # If count is 123, the code is {math_code}_1_2_3
    digits = list(str(count))
    count_str = "_".join(digits)
    return f'{math_code}_{count_str}'


def modify_text(text, modify_func):
    # modify text without touching the variable codes
    split_text = [s for s in re.split(match_code, text) if s is not None]
    for i in range(len(split_text)):
        if not re.match(match_code, split_text[i]):
            split_text[i] = modify_func(split_text[i])
    text = "".join(split_text)
    return text


def modify_before(text):
    # mathpix is stupid so sometimes does not add $ $ for \pm
    text = text.replace('\\pm', '$\\pm$')
    # the "." may be treated as end of sentence
    text = text.replace('Eq.', 'equation')
    return text


def modify_after(text):
    # the "_" in the text should be replaced to "\_"
    pattern = r"(?<!\\)_"
    text = re.sub(pattern, r"\\_", text)
    return text


def replace_latex_objects(text, brace=True, command_simple=True):
    r"""
    Replaces all LaTeX objects in a given text with the format "{math_code}_{digit1}_{digit2}_..._{digit_last}",
    applies a given function to the resulting text (excluding the "{math_code}_{digit1}_{digit2}_..._{digit_last}" parts),
    and returns both the processed text and a list of replaced LaTeX objects.
    Supported LaTeX objects: \[ xxx \], \begin{xxx} \end{xxx}, $$ $$,
    $ $, \( xxx \), \xxx[xxx]{xxx}, \xxx{xxx}, and \xxx.
    Returns the processed text and a list of replaced LaTeX objects.
    """

    # You need to make sure that the input does not contain {math_code}
    # define regular expressions for each LaTeX object
    patterns_mularg_command = [get_pattern_command_full(name, n) for name, n, index in config.mularg_command_list]
    latex_obj_regex = [
        r"\$\$(.*?)\$\$",  # $$ $$
        r"\$(.*?)\$",  # $ $
        r"\\\[(.*?)\\\]",  # \[ xxx \]
        r"\\\((.*?)\\\)",  # \( xxx \)
        pattern_env,  # \begin{xxx} \end{xxx}
        pattern_set1,
        pattern_set2,
    ] + patterns_mularg_command + [pattern_command_full]  # \xxx[xxx]{xxx}
    if brace:
        latex_obj_regex.append(pattern_brace)
    if command_simple:
        latex_obj_regex.append(pattern_command_simple)  # \xxx

    # iterate through each LaTeX object and replace with "{math_code}_{digit1}_{digit2}_..._{digit_last}"
    count = 0
    replaced_objs = []
    for regex_symbol in latex_obj_regex:
        pattern = regex.compile(regex_symbol, regex.DOTALL)
        while pattern.search(text):
            latex_obj = pattern.search(text).group()
            replaced_objs.append(f' {latex_obj} ')
            text = pattern.sub(' ' + variable_code(count) + ' ', text, 1)
            count += 1

    text = modify_text(text, modify_before)
    return text, replaced_objs


def recover_latex_objects(text, replaced_objs, tolerate_error=False):
    # recover the latex objects from "replace_latex_objects"
    nobjs = len(replaced_objs)
    matched_indices = []

    def get_obj(digit_str):
        index = int(''.join(digit_str.split('_')))
        matched_indices.append(index)
        if index < nobjs:
            return replaced_objs[index]
        else:
            if test_environment:
                assert tolerate_error
            return '???'

    text = modify_text(text, modify_after)
    pattern = re.compile(match_code_replace)
    # count number of mismatch
    total_num = 0
    while True:
        text, num_modify = pattern.subn(lambda match: get_obj(match.group(1)), text)
        total_num += num_modify
        if num_modify == 0:
            break
    n_good = len(set(matched_indices).intersection(set(range(nobjs))))
    n_bad1 = len(matched_indices) - n_good
    n_bad2 = nobjs - n_good
    n_bad = max(n_bad1, n_bad2)
    return text, n_bad, nobjs


def remove_tex_comments(text):
    """
    Removes all TeX comments in a given string with the format "% comment text".
    Does not match "\%".
    If "%" is at the beginning of a line then delete this line.
    Returns the processed string.
    """
    text = text.replace(r'\\', f'{math_code}_BLACKSLASH')
    text = text.replace(r'\%', f'{math_code}_PERCENT')
    text = re.sub(r"\n\s*%.*?(?=\n)", "", text)
    text = re.sub(r"%.*?(?=\n)", "", text)
    text = text.replace(f'{math_code}_PERCENT', r'\%')
    text = text.replace(f'{math_code}_BLACKSLASH', r'\\')

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


def process_specific_env(latex, function, env_name):
    # find all patterns of \begin{env_name}[options] content \end{env_name}
    # then replace `content` by `function(content)`
    pattern = regex.compile(get_pattern_env(env_name), regex.DOTALL)

    def process_function(match):
        name = match.group(1)
        assert re.match(env_name, name)
        options = match.group(2)
        if options is None:
            options = ''
        content = match.group(3)
        processed_content = function(content)
        return rf'\begin{{{env_name}}}{options}{processed_content}\end{{{env_name}}}'
    return pattern.sub(process_function, latex)


def process_specific_command(latex, function, command_name):
    # find all patterns of # \{command_name}[options]{content}
    # then replace `content` by `function(content)`
    pattern = regex.compile(get_pattern_command_full(command_name), regex.DOTALL)

    def process_function(match):
        name = match.group(1)
        assert re.match(command_name, name)
        options = match.group(2)
        if options is None:
            options = ''
        content = match.group(4)
        processed_content = function(content)
        return rf'\{command_name}{options}{{{processed_content}}}'
    return pattern.sub(process_function, latex)


def process_mularg_command(latex, function, command_tuple):
    # find all patterns of # \{command_name}[options]{content}
    # then replace `content` by `function(content)`
    command_name, nargs, args_to_translate = command_tuple
    pattern = regex.compile(get_pattern_command_full(command_name, n=nargs), regex.DOTALL)

    def process_function(match):
        name = match.group(1)
        assert re.match(command_name, name)
        group_index = 2
        contents = []
        for i in range(nargs):
            content = match.group(group_index + 1)
            if i in args_to_translate:
                content = function(content)
            contents.append(content)
            group_index += 2
        return rf'\{command_name}' + ''.join([rf'{{{content}}}' for content in contents])
    return pattern.sub(process_function, latex)


def process_leading_level_brace(latex, function):
    # leading level means that the {xxx} is not inside other objects, i.e. \command{} or \begin{xxx} \end{xxx}
    # replace `{ content }` by `{ function(content) }`
    text, envs = replace_latex_objects(latex, brace=False)
    braces_content = []
    count = 0

    def process_function(match):
        nonlocal braces_content, count
        content = match.group(1)
        # function here is translate_paragraph_latex, which cannot contain replaced environments
        processed_content = function(recover_latex_objects(content, envs)[0])
        result = rf'{{ {processed_content} }}'
        braces_content.append(result)
        placeholder = f'BRACE{count}BRACE'
        count += 1
        return placeholder

    text = regex.compile(pattern_brace, regex.DOTALL).sub(process_function, text)
    latex = recover_latex_objects(text, envs)[0]
    for i in range(count):
        latex = latex.replace(f'BRACE{i}BRACE', braces_content[i])
    return latex


def split_by_command(latex):
    # split by things like \item
    text, envs = replace_latex_objects(latex, command_simple=False)

    texts = [(text, '')]

    for pattern, command in [(r'\\item\s+', '\item')]:
        new_texts = []
        for t, sep in texts:
            splited_t = re.split(pattern, t)
            seps = [command for _ in splited_t]
            seps[-1] = sep
            new_texts += list(zip(splited_t, seps))
        texts = new_texts

    seps = [t[1] for t in texts]
    texts = [t[0] for t in texts]
    latexs = [recover_latex_objects(t, envs)[0] for t in texts]
    return latexs, seps


def remove_blank_lines(text):
    pattern = re.compile(r'\n\n+')
    text = pattern.sub('\n', text)
    return text


def insert_macro(text, macro):
    pattern = re.compile(r"\\document(class|style)(\[.*?\])?\{(.*?)\}", re.DOTALL)
    match = pattern.search(text)
    assert match is not None
    start, end = match.span()
    new_text = text[:end] + f"\n{macro}\n" + text[end:]
    return new_text


def is_complete(latex_code):
    # Define regular expressions for \documentclass, \begin{document}, and \end{document}
    documentclass_pattern = re.compile(r"\\document(class|style)(\[.*?\])?\{.*?\}", re.DOTALL)
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


def get_theorems(text):
    pattern = re.compile(pattern_theorem, re.DOTALL)
    matches = re.finditer(pattern, text)
    theorems = [match.group(1) for match in matches]
    return theorems


def get_nonNone(*args):
    result = [arg for arg in args if arg is not None]
    assert len(result) == 1
    return result[0]


def replace_special(text):
    for special in list_special:
        # add space around
        text = text.replace(f'\\{special}', f' {math_code}{special_character_forward[special]} ')

    return text


def recover_special(text):
    for special in list_special:
        text = text.replace(math_code + special_character_forward[special], f'\\{special}')

    return text


def replace_accent(text):
    def replace_function(match):
        # if it is \"{o}, then special is ", char1 is o, char2 is None
        # if it is \"o, then special is ", char1 is None, char2 is o
        special = match.group(1)
        char1 = match.group(2)
        char2 = match.group(3)
        char = get_nonNone(char1, char2)
        # do not add space around
        return math_code + special_character_forward[special] + f'{char}'

    text = re.compile(pattern_accent).sub(replace_function, text)

    return text


def recover_accent(text):
    def replace_function(match):
        try:
            special = special_character_backward[match.group(1)]
            char = match.group(2)
            return rf'\{special}{{{char}}}'
        except Exception:
            return ''

    text = re.compile(match_code_accent).sub(replace_function, text)

    return text


def combine_split_to_sentences(text):
    # if two lines are separately by only one \n, in latex they are in the same paragraph so we combine them in the same line
    # However we don't combine them if the second line does not start from normal letters (so usually some latex commands)
    n = len(math_code)
    pattern = re.compile(r'\n(\s*([^\s]+))')

    def process_function(match):
        string = match.group(2)
        if string[0:n] == math_code:
            return match.group(0)
        else:
            return ' ' + match.group(1)

    return pattern.sub(process_function, text)


def delete_specific_format(latex, format_name):
    pattern = regex.compile(get_pattern_command_full(format_name), regex.DOTALL)
    return pattern.sub(lambda m: ' ' + m.group(4) + ' ', latex)


def replace_newcommand(newcommand, latex):
    command_name, n_arguments, content = newcommand
    pattern = regex.compile(get_pattern_command_full(command_name, n_arguments), regex.DOTALL)

    def replace_function(match):
        this_content = content
        name = match.group(1)
        assert re.match(command_name, name)
        for i in range(n_arguments):
            text = match.group(3 + i * 2)
            this_content = this_content.replace(f'#{i+1}', f' {text} ')
        return this_content

    return pattern.sub(replace_function, latex)


def process_newcommands(latex):
    pattern = regex.compile(pattern_newcommand, regex.DOTALL)
    count = 0
    full_newcommands = []
    matches_all = list(regex.finditer(pattern, latex))
    for match in matches_all:
        need_replace = False
        content_all = match.group(0)
        for special in replace_newcommand_list:
            if special in content_all:
                need_replace = True
        if not need_replace:
            continue
        name1 = match.group(1)
        name2 = match.group(2)
        name = get_nonNone(name1, name2)
        n_arguments = match.group(3)
        if n_arguments is None:
            n_arguments = 0
        else:
            n_arguments = int(n_arguments)
        content = match.group(5)
        latex = latex.replace(match.group(), f'{math_code}_REPLACE{count}_NEWCOMMAND')
        full_newcommands.append(match.group(0))
        latex = replace_newcommand((name, n_arguments, content), latex)
        count += 1
    for i in range(count):
        latex = latex.replace(f'{math_code}_REPLACE{i}_NEWCOMMAND', full_newcommands[i])
    return latex


def remove_bibnote(latex):
    pattern = regex.compile(get_pattern_command_full('bibinfo', 2), regex.DOTALL)

    def replace_function(match):
        assert match.group(1) == 'bibinfo'
        if match.group(3) == 'note':
            return ''
        else:
            return match.group(0)
    return pattern.sub(replace_function, latex)
