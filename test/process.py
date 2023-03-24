import mathtranslate
import re
old = r"""
This is a paragraph with some L_a_T_e_X environments:
\begin{enumerate}
\item First item
\item Second item
\end{enumerate}
And some math: $E=mc^2$ and $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
"""
new = r"""
THIS IS A PARAGRAPH WITH SOME L\_A\_T\_E\_X ENVIRONMENTS:
\begin{enumerate}
\item First item
\item Second item
\end{enumerate}
AND SOME MATH: ??? AND $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
$ H \psi = E \psi$
"""
text1, eqs = mathtranslate.process_latex.replace_latex_envs(old)
text2 = re.sub(r'XMATHX_2(?![\d_])', 'XMATHX_2_2', text1)
text3 = text2.upper()
text4 = mathtranslate.process_latex.recover_latex_envs(text3, eqs)
assert text4 == new
