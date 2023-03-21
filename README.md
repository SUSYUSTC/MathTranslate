# MathTranslate

<p align="center">
  <!-- tests (GitHub actions) -->
  <a href="https://github.com/SUSYUSTC/MathTranslate/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/SUSYUSTC/MathTranslate/ci.yml?branch=master" />
  </a>
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

**Since google translate cannot be used in China mainland, we will add support of other translation engines as soon as possible.**

This is a project to provide translation of scientific papers with heavy math symbols from any language to any language while keeping the math symbols unchanged. In most translation softwares you wouldn't be able to keep equations and it would annoy you.
This project is based on the following two tools:
1. [mathpix](https://mathpix.com/): it provides an interface to convert text+equation images to latex code. Unfortunately, it is not totally free. The price can be seen at  https://mathpix.com/pricing. In further developments, we will try our best to reduce the number of requests to save your money. (This project itself is 100% free and open-source!)
2. google translate

The main work of this project is to translate LaTex files based on Google Translate of plain text, with mathpix combined we can finally translate pdf (or other formats) to pdf.

Here's an example of what you get finally.
<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

Although it is currently a small project, we are aware that this project has received much more attention that we expected. We are planning more developments for better user experience.

## Releases
### Mar 16, 2023
We are now supporting all operating systems! Now you can install simply by `pip install mathtranslate`.

## Requirements
1. A [mathpix](https://mathpix.com/) account. Unfortunately, it is not totally free. The current price is free for 100 screenshots (requires an educational email in registeration) and $5 per month for 5000 screenshots.
2. Python3 and pip.
3. texlive (or any other tool to generate pdf from tex). For Chinese you would need CJK package.

## Installation
`pip install mathtranslate`

## Usage
1. Download mathpix. In the Settings-Formatting, change "Inline math delimiters" and "Block mode delimiters" to "\\( ... \\)" and "\\[ ... \\]", respectively.
<img src="https://user-images.githubusercontent.com/30529122/225747242-07b89c34-4f16-40f9-bebc-d0c0b1c4c8e8.png" width="600">

2. Use mathpix to screenshot what you want to translate, copy the output latex code and save in a txt file. Mathpix currently recognizes continuous text (which can be one or more paragraphs). You can also screenshot and copy multiple separated texts and put them in the same txt file, we will automatically identify and merge the paragraphs separated by pictures or pages in the next step.
3. Assume the filename you saved in the previous step is `main.txt`. Run `translate_tex.py main.txt`. You will get a translated tex file `main.tex` and a corresponding pdf file `main.pdf` in case `xelatex` is installed on your machine.
4. Since this project is small, sometimes you need to slightly change the final tex file for compilation.
5. The default behavior is translating English into Chinese. If you want to translate from/to other languages, you can use `translate_tex.py --list` to find the code of your interested language and then run `translate_tex.py main.txt -from <code_from> -to <code_to>`.

## Examples
In the example directory, you can see `main.txt` which is the mathpix output of a part of `paper.pdf`. Run `translate_tex.py main.txt` and you will get the `main.tex` and `main.pdf`. `translated.png` is what you should expect to see in the `main.pdf`.

## Further developments
1. Automatically extract images from pdf, process images in a batch and output a single translated pdf by one click!
2. Reduce the number of mathpix requests by open-source techniques.
3. A more user-friendly interface.

If you are interested in making contributions, please contact me by susyustc@gmail.com.
