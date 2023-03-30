import mathtranslate
mathtranslate.process_latex.test_environment = False
import mathtranslate.process_latex as pl
import re
old = open("./old.txt").read()
new = open("./new.txt").read()
text1, eqs = mathtranslate.process_latex.replace_latex_objects(old)
text2 = re.sub(r'XMATHX_2(?![\d_])', 'XMATHX_2_2', text1)
text3 = text2.upper()
text4 = mathtranslate.process_latex.recover_latex_objects(text3, eqs)
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
