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
2. (IP users in Mainland China): [Tencent Translation API](https://cloud.tencent.com/product/tmt) account. After registration, you can get the secret ID and secret key in [Tencent Console](https://console.cloud.tencent.com/cam/capi). Tencent Translate is the translation API with the highest free quota in our knowledge besides Google Translate, with a free quota of 5 million characters per month, and no fee will be deducted if there is no manual recharge (that is, there is no need to worry about misuse).

## Installation
`pip install --upgrade mathtranslate`

## Usage
1. Prepare or generate a tex file. You can get the tex file by the following two ways:
     - For most [arxiv](https://arxiv.org/) papers, you can download the latex source code (Download - Other formats - Source). If the file you downloaded has no suffix, in most cases it is in .tar format, you may need to add the suffix manually. After decompression you can get a latex project, and then you can translate the .tex files in it.
     - Use [mathpix](https://mathpix.com/) to take a screenshot of the part you want to translate. You can capture many connected segments at one time, or combine multiple screenshots into one file. Unfortunately, it's not completely free. Currently mathpix offers 100 screenshots for free (an edu email is required for registration) or 5000 screenshots for $5 per month.
2. (Tencent Translate API users) run `translate_tex --setkey` to store the API ID and key.
3. Translate the tex file by `translate_tex input.tex -o output.tex`.
4. Compile your tex file. You can compile it with the texlive command `xelatex output.tex`. For Chinese you need the xeCJK package. If it is a downloaded arxiv project, we recommend compressing all files into a zip file and uploading it to overleaf for online compilation. **Note, you need to set the XeLatex compiler in `Menu - Compiler`, otherwise it cannot handle other languages. **
5. You can change the default settings of the translation language and engine through the command line parameters `-engine`, `-from`, `-to`. For example `translate_tex -engine tencent input.tex -o output.tex`. You can also permanently change the setting via `translate_tex --setdefault`. You can see more details with `translate_tex --help`.

## Examples
In the example directory, you can see `main.txt` which is the mathpix output of a part of `paper.pdf`. Run `translate_tex main.txt` and you will get the `main.tex` and `main.pdf`. `translated.png` is what you should expect to see in the `main.pdf`.

## Further developments
1. Automatically extract images from pdf, process images in a batch and output a single translated pdf by one click!
2. Reduce the number of mathpix requests by open-source techniques.
3. A more user-friendly interface.

If you have any questions or have interests in making contributions, please contact me by susyustc@gmail.com or joining QQ group 288646946.
