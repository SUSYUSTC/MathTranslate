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

The main work of this project is to translate LaTeX files based on Google Translate in plain text, and finally realize the translation of pdf.

Here's an example of what you get finally.

<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/227698548-1cc19f7c-00e7-4312-9d58-2a7237656b51.png" width="700">
</p>

<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

## Releases
### May 14, 2023
We add the ability to directly translate the whole arxiv project with just one click.
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
`pip install --upgrade mathtranslate`

## Usage
1. Prepare or generate a tex file or project. You can obtain a tex file or project in the following ways:
    - For most [arxiv](https://arxiv.org/) papers, the latex source code is public, and we provide a simple API to translate the entire project with just one click using an arxiv number.
    - Use [mathpix](https://mathpix.com/) to convert the pdf you want to translate into latex code. Mathpix can directly convert pdf to latex code or convert a screenshot into code. Unfortunately, mathpix requires a fee after exceeding a certain amount of usage. Here is the [price list](https://mathpix.com/pricing).
2. (For Tencent Translation API users) Run `translate_tex --setkey` to store the API secretID and secretKey.
3. Translate the tex file or project in command line.
   - To translate a single file: `translate_tex input.tex -o output.tex` will generate a translated tex file `output.tex`.
   - To translate an arxiv project: `translate_arxiv 2205.15510` will generate a translated tex project `2205.15510.zip`.
4. Compile your tex file. For a single file, you can use the command `xelatex output.tex` from [texlive](https://www.tug.org/texlive/). Chinese translation requires the xeCJK package. For arxiv projects, we recommend uploading the obtained .zip file to overleaf for online compilation (New Project - Upload Project). **Note that you need to set the compiler to XeLatex in `Menu - Compiler`.**
5. You can change the default settings of translation language and engine through command line arguments `-engine`, `-from`, `-to`. For example, `translate_tex -engine tencent input.tex -o output.tex`. You can also permanently change the settings through `translate_tex --setdefault`. You can view more details through `translate_tex --help`. `translate_arxiv` also provides exactly the same command line arguments, which have the same effect.

## Examples
In the example directory, you can see `main.txt` which is the mathpix output of a part of `paper.pdf`. Run `translate_tex main.txt` and you will get the `main.tex` and `main.pdf`. `translated.png` is what you should expect to see in the `main.pdf`.

## Further developments
1. Fix bugs in the latex translations.
2. A more user-friendly interface.

If you have any questions or have interests in making contributions, please contact me by susyustc@gmail.com or joining QQ group 288646946.

## Donation
If you think this project is helping you a lot, you can support us by the Wechat QR code below
<p align="center">
  <img width=30% src="https://github.com/SUSYUSTC/MathTranslate/assets/30529122/16f82637-e102-4330-82ad-bbcbdad1c19d">
</p>
