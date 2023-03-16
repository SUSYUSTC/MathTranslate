# MathTranslate
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.md)
[![zh](https://img.shields.io/badge/lang-zh-yellow.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.zh.md)

This is a project to provide translation of scientific papers with heavy math symbols from any language to any language while keeping the math symbols unchanged. In most translation softwares you wouldn't be able to keep equations and it would annoy you.
This project is based on the following two tools:
1. mathpix: it provides an interface to convert text+equation images to latex code.
2. translate-shell: it provides a terminal interface to google translate

The main work in this project is to translate a latex file from one language to another and to develop an interface of the above two tools.

Here's an example of what you get finally.
<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/225237425-9341b03e-25b5-4617-b606-5e3813de3ec2.png" width="260">
<img src="https://user-images.githubusercontent.com/30529122/225234174-78af1e5f-aeff-4dd8-9f4c-d948edc35318.png" width="400">
</p>

## Requirements
1. A mathpix account with OCR https://mathpix.com/docs/ocr/overview
2. python 3 with library `requests`: `pip install requests`
3. translate-shell: `sudo apt-get install translate-shell`
4. texlive (or any other tool to generate pdf from tex): `sudo apt-get install texlive-full`

## Usage
1. In `MathTranslate/scripts/mpix.py`, replace 'YOUR_APP_ID' and 'YOUR_APP_KEY' with the OCR ID and key you get from mathpix website (the rate limit is 200 times per minute which is more than enough unless you want to translate a huge batch)
2. Add directory `MathTranslate/scripts` to PATH
3. Screenshot each part of your paper one by one and name them by part1.png, part2.png, ... partXXX.png in your directory as showed in the following figure. Basically each screenshot is half-page/one-page depending the paper layout and you just need to avoid including figures. Later developments will simplify this process and finally use single pdf as input.
<img src="https://user-images.githubusercontent.com/30529122/225232807-88c1dba4-f513-4688-9c6c-6dc7fa708cda.png" width="500">

4. Run `translate.sh` in this folder then `main.pdf` (and `main.tex`) is all you need!
5. Since this project is small, sometimes you need to slightly change the final tex file for compilation.
6. The default code is translating English into Chinese. If you want to translate from/to other languages, you just need to change `language_from` and `language_to` in `MathTranslate/scripts/translate_tex.py`

## Features
1. If your screenshot images are in order, the paragraphs splited by pages/figures will be automatically connected
2. The mathpix generation operation (which is time-consuming) is cached. This means that you don't have to run the whole stuff again if you only add 1 additional screenshot. You could just try 1-2 at the beginning and then decide whether to add more.

## Examples
In the example directory, run `translate.sh` and you would expect to get the same with `main.tex` and `main.pdf`.

## Further developments
1. Make it compatible on different operating systems
2. Automatically extract text boxes from pdf file to avoid screenshots
3. Make it more user-friendly

If you are interested in making contribution, please contact me by susyustc@gmail.com.
