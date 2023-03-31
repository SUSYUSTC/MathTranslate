# MathTranslate

<p align="center">
  <!-- PyPI -->
  <a href="https://pypi.org/project/mathtranslate/">
    <img src="https://img.shields.io/pypi/v/mathtranslate.svg?logo=pypi"/>
  </a>
  <!-- License -->
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-yellow.svg?logo=apache"/>
  </a>
</p>


<p align="center">
  <a href="https://github.com/SUSYUSTC/MathTranslate">
    <img width=30% src="logo.jpg">
  </a>
</p>

<p align="center"> English | <a href="README.zh.md"> 简体中文 </a></p>

This is a project to provide translation of scientific papers with heavy math symbols from any language to any language while keeping the math symbols unchanged. In most translation softwares you wouldn't be able to keep equations and it would annoy you.

The main work of this project is to translate LaTex files based on Google Translate in plain text, and finally realize the translation of pdf.

Here's an example of what you get finally.

<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/227698548-1cc19f7c-00e7-4312-9d58-2a7237656b51.png" width="700">
</p>

<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

Although it is currently a small project, we are aware that this project has received much more attention that we expected. We are planning more developments for better user experience.

## Releases
### Mar 24, 2023
We add the ability to directly translate arxiv papers.
### Mar 21, 2023
We add tencent translation option for users with IP in China mainland.
### Mar 16, 2023
We are now supporting all operating systems! Now you can install simply by `pip install --upgrade mathtranslate`.

## Requirements
1. Python3 and pip. [Anaconda](https://www.anaconda.com) is recommended.
2. (For users with IP in Mainland China): [Tencent Translation API](https://cloud.tencent.com/product/tmt) account. After registration, you can get the secret ID (not the APP ID!) and secret Key in [Tencent Console](https://console.cloud.tencent.com/cam/capi). Tencent Translate is the translation API with the highest free quota to our knowledge besides Google Translate, with a free quota of 5 million characters per month, and no fee will be deducted if there is no manual recharge (that is, there is no need to worry about misuse).

## Installation & Update
`pip install --upgrade mathtranslate -i https://pypi.org/simple`

**We suggest the users to always check update before using because we update frequently**

## Usage
1. Prepare or generate a tex file. You can get the tex file by the following two ways:
     - For most [arxiv](https://arxiv.org/) papers, you can download the latex source code (Download - Other formats - Source). If the file you downloaded has no suffix, in most cases it is in .tar format, you may need to add the suffix manually. After decompression you can get a latex project, and then you can translate the .tex files in it.
     - Use [mathpix](https://mathpix.com/) to convert the pdf you want to translate into latex code. mathpix can directly convert pdf page into latex code or convert screenshots into code. We can handle both of these methods. Unfortunately, mathpix charges after a certain amount of usage, here is the [price](https://mathpix.com/pricing).
2. (Tencent Translate API users) run `translate_tex --setkey` to store the API secretID and secretKey.
3. Translate the tex file by `translate_tex input.tex -o output.tex`.
4. Compile your tex file. You can compile it with the  [texlive](https://www.tug.org/texlive/) command `xelatex output.tex`. For Chinese you need the xeCJK package. If it is a downloaded arxiv project, we recommend compressing all files into a zip file and uploading it to [overleaf](https://www.overleaf.com/project) for online compilation. **Note, you need to set the XeLatex compiler in `Menu - Compiler`, otherwise it cannot handle other languages.**
5. You can change the default settings of the translation language and engine through the command line arguments `-engine`, `-from`, `-to`. For example `translate_tex -engine tencent input.tex -o output.tex`. You can also permanently change the setting via `translate_tex --setdefault`. You can see more details with `translate_tex --help`.

## Examples
In the example directory, you can see `main.txt` which is the mathpix output of a part of `paper.pdf`. Run `translate_tex main.txt` and you will get the `main.tex` and `main.pdf`. `translated.png` is what you should expect to see in the `main.pdf`.

## Known Issues
1. If `\begin{env} \end{env}` is reset with `\newcommand` in latex, it will not be translated correctly.
2. There is a small probability to get something like "XMATHX_1_2" or wrong formula during translation. The accuracy rate of Tencent translation is slightly lower than that of Google translation.

## Further developments
1. Fix bugs in the latex translations.
2. A more user-friendly interface.

If you have any questions or have interests in making contributions, please contact me by susyustc@gmail.com or joining QQ group 288646946.
