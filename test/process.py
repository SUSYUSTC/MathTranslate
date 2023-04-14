import mathtranslate
mathtranslate.process_latex.test_environment = False
import mathtranslate.process_latex as pl
import re
import regex
old = open("./old.txt").read()
new = open("./new.txt").read()
text1, eqs = mathtranslate.process_latex.replace_latex_objects(old)
text2 = re.sub(r'XMATHX_2(?![\d_])', 'XMATHX_2_2', text1)
text3 = text2.upper()
text4 = mathtranslate.process_latex.recover_latex_objects(text3, eqs)[0]
assert text4 == new

old_special = r'\\ \ \& \%'
new_special = r' \\   \   \&   \% '
intermediate = pl.replace_special(old_special)
assert intermediate.count(mathtranslate.config.math_code) == 4
assert pl.recover_special(intermediate) == new_special

old_accent = r'\^{o} \^o \"{o} \"o'
new_accent = r'\^{o} \^{o} \"{o} \"{o}'
intermediate = pl.replace_accent(old_accent)
assert intermediate.count(mathtranslate.config.math_code) == 4
assert pl.recover_accent(pl.replace_accent(old_accent)) == new_accent


newcommand1 = r'\newcommand {\partder} [2] {\frac{\partial #1}{\partial #2}}'
newcommand2 = r'\def {\ket} [1] {\left | {#1} \right \rangle }'
newcommand3 = r'\newcommand \refstate {\textbf{0}}'
newcommand4 = r'\newcommand{\ee}{\end{equation}}'
ref1 = ('partder',
        None,
        '2',
        '{\\frac{\\partial #1}{\\partial #2}}',
        '\\frac{\\partial #1}{\\partial #2}')
ref2 = ('ket',
        None,
        '1',
        '{\\left | {#1} \\right \\rangle }',
        '\\left | {#1} \\right \\rangle ')
ref3 = (None, 'refstate', None, '{\\textbf{0}}', '\\textbf{0}')
ref4 = ('ee', None, None, '{\\end{equation}}', '\\end{equation}')
assert regex.match(mathtranslate.process_latex.pattern_newcommand, newcommand1).groups() == ref1
assert regex.match(mathtranslate.process_latex.pattern_newcommand, newcommand2).groups() == ref2
assert regex.match(mathtranslate.process_latex.pattern_newcommand, newcommand3).groups() == ref3
assert regex.match(mathtranslate.process_latex.pattern_newcommand, newcommand4).groups() == ref4

latex = r'''
\newcommand {\partder} [2] {\frac{\partial #1}{\partial #2}}
\def {\ket} [1] {\left | {#1} \right \rangle }
\newcommand \refstate {\textbf{0}}
\newcommand{\ee}{\end{equation}}

\partder {arg{1}} {arg{2}}
\ket {arg{1}}
\refstate
\ee
\eeabc
'''
ref = '\n\\newcommand {\\partder} [2] {\\frac{\\partial #1}{\\partial #2}}\n\\def {\\ket} [1] {\\left | {#1} \\right \\rangle }\n\\newcommand \\refstate {\\textbf{0}}\n\\newcommand{\\ee}{\\end{equation}}\n\n\\frac{\\partial arg{1}}{\\partial arg{2}}\n\\left | {arg{1}} \\right \\rangle \n\\textbf{0}\n\\end{equation}\n\\eeabc\n'
assert mathtranslate.process_latex.process_newcommands(latex) == ref
