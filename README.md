# MathTranslate
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.md)
[![zh](https://img.shields.io/badge/lang-zh-yellow.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.zh.md)

<p align="center">
  <a href="https://github.com/SUSYUSTC/MathTranslate">
    <img width=30% src="logo.jpg">
  </a>
</p>


This is a project to provide translation of scientific papers with heavy math symbols from any language to any language while keeping the math symbols unchanged. In most translation softwares you wouldn't be able to keep equations and it would annoy you.
This project is based on the following two tools:
1. [mathpix](https://mathpix.com/): it provides an interface to convert text+equation images to latex code. Unfortunately it is not totally free. The price can be seen at  https://mathpix.com/pricing. In further developments we will try our best to reduce the number of requests to save your money. (This project itself is 100% free and open-source!)
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
We are now supporting all operating systems! You only need to have python and pip to do everything.

## Requirements
1. A [mathpix](https://mathpix.com/) account. Unfortunatedly it is not totally free. The current price is free for 100 screenshots (requires an educational email in registeration) and $5 per month for 5000 screenshots.
2. Python3 and library `mtranslate`: `pip install mtranslate`
3. texlive (or any other tool to generate pdf from tex). For Chinese you would need CJK package.

## Usage
1. Download mathpix. In the Settings-Formatting, change "Inline math delimiters" and "Block mode delimiters" to "\\( ... \\)" and "\\[ ... \\]", respectively.
<img src="https://user-images.githubusercontent.com/30529122/225747242-07b89c34-4f16-40f9-bebc-d0c0b1c4c8e8.png" width="600">

2. Add directory `MathTranslate/scripts` to PATH
3. Use mathpix to screenshot what you want to translate, copy the output latex code and save in a txt file. Mathpix currently recognizes continuous text (which can be one or more paragraphs). You can also screenshot and copy multiple separated texts and put them in the same txt file, we will automatically identify and merge the paragraphs separated by pictures or pages in the next step.
4. Assume the filename you saved in the previous step is `main.txt`. Run `translate_tex.py main.txt`. You will get a translated tex file `main.tex` and a corresponding pdf file `main.pdf` in case `xelatex` is installed on your machine.
5. Since this project is small, sometimes you need to slightly change the final tex file for compilation.
6. The default code is translating English into Chinese. If you want to translate from/to other languages, you just need to change `language_from` and `language_to` in `MathTranslate/scripts/translate_tex.py`

## Examples
In the example directory, you can see `main.txt` which is the mathpix output of a part of `paper.pdf`. Run `translate_tex.py main.txt` and you will get the `main.tex` and `main.pdf`. `translated.png` is what you should expect to see in the `main.pdf`.

## Further developments
1. Automatically extract images from pdf, process images in a batch and output a single translated pdf by one click!
2. Reduce the number of mathpix requests by open-source techniques.
3. A more user-friendly interface.

If you are interested in making contributions, please contact me by susyustc@gmail.com or Wechat account sunjiace2262.
