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
  <!-- GUI -->
  <a href="https://github.com/SUSYUSTC/MathTranslate/releases">
    <img src="https://img.shields.io/badge/GUI-v3.1.0-red.svg?logo=apache"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/SUSYUSTC/MathTranslate">
    <img width=30% src="logo.jpg">
  </a>
</p>

<p align="center"> English | <a href="README.zh.md"> 简体中文 </a></p>

<p align="center"> <a href="https://github.com/SUSYUSTC/MathTranslate/releases"> GUI download address </a></p>

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
### Jun 24, 2023
We release the [GUI](https://github.com/SUSYUSTC/MathTranslate/releases) for MathTranslate. You can open it directly without installing anything!
### May 14, 2023
We add the ability to directly translate the whole arxiv project with just one click.
### Mar 24, 2023
We add the ability to directly translate arxiv papers.
### Mar 21, 2023
We add tencent translation option for users with IP in China mainland.
### Mar 16, 2023
We are now supporting all operating systems! Now you can install simply by `pip install --upgrade mathtranslate`.

## 这里是[中文介绍地址](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.zh.md)

## Backend engine
The default engine is google translate, which can not be accessed with IP in mainland China. For users with IP in mainland China we provide the tencent engine, although its accuracy is not as good as the google engine. 
To use the tencent engine, you need to register the [Tencent Translation API](https://cloud.tencent.com/product/tmt) account. After registration, you can get the secret ID (not the APP ID!) and secret Key in [Tencent Console](https://console.cloud.tencent.com/cam/capi). Tencent Translate is the translation API with the highest free quota to our knowledge besides Google Translate, with a free quota of 5 million characters per month, and no fee will be deducted if there is no manual recharge (that is, there is no need to worry about misuse).

## proxy settings
If you plan to use google engine by setting a proxy, you may need to set environment variables, otherwise the proxy may not work outside of the browser. The environment variables that need to be set are `http_proxy` and `https_proxy`, for example
```
export http_proxy=http://127.0.0.1:7890
export https_proxy=https://127.0.0.1:7890
```
The proxy address and port will be different according to different proxy software. In Windows, environment variables can also be set in a non-command-line manner.

## GUI Installation
Simply [download](https://github.com/SUSYUSTC/MathTranslate/releases) the corresponding executable file and you are done!

## GUI usage

https://github.com/SUSYUSTC/MathTranslate/assets/30529122/04c1971d-b094-41d8-bdbb-6dd65d4b81c4

You can set the translation engine and language in the **Preference** page. If you plan to use the tencent engine, you need to set the secret ID and secret Key.
1. If you want to translate a paper on [arxiv](https://arxiv.org/), you can use the **Arxiv Translate** function. You just need to enter the arxiv number of the paper you want to translate (for example 2205.15510). After the translation you will get a `.zip` file, which contains the latex source code of the arxiv project.
2. If you want to translate a paper only with pdf version, you can first convert the pdf to latex by [mathpix](https://mathpix.com/) and then use the **File Translate** function. Unfortunately, mathpix requires a fee after exceeding a certain amount of usage. Here is the [price list](https://mathpix.com/pricing). After the translation you will get a `.tex` file which contains the corresponding latex file.

After the translation is done you can upload either the `.zip` (New Project - Upload Project) or `.tex` (New Project - Blank Project and copy-paste) file to [overleaf](https://www.overleaf.com/project) for online compilation.
**Note: you have to set the compiler to XeLatex in `Menu - Compiler`.**

## Command line installation
1. Install python3 and pip.
2. `pip install --upgrade mathtranslate`

## Command line usage
**For Windows user you may need to run cmd or powershell as administrator.**
1. Prepare or generate a tex file or project. You can obtain a tex file or project in the following ways:
    - For most [arxiv](https://arxiv.org/) papers, the latex source code is public, and we provide a simple API to translate the entire project with just one click using an arxiv number.
    - Use [mathpix](https://mathpix.com/) to convert the pdf you want to translate into latex code. Mathpix can directly convert pdf or screenshot to latex code. Unfortunately, mathpix requires a fee after exceeding a certain amount of usage. Here is the [price list](https://mathpix.com/pricing).
2. (For Tencent Translation API users) Run `translate_tex --setkey` to store the API secretID and secretKey.
3. Translate the tex file or project in command line.
   - To translate a single file: `translate_tex input.tex -o output.tex` will generate a translated tex file `output.tex`.
   - To translate an arxiv project: `translate_arxiv 2205.15510` will generate a translated tex project `2205.15510.zip`.
4. Compile your tex file. For a single file, you can use the command `xelatex output.tex` from [texlive](https://www.tug.org/texlive/). Chinese translation requires the xeCJK package. For arxiv projects, we recommend uploading the obtained .zip file to overleaf for online compilation (New Project - Upload Project). **Note that you need to set the compiler to XeLatex in `Menu - Compiler`.**
5. You can change the default settings of translation language and engine through command line arguments `-engine`, `-from`, `-to`. For example, `translate_tex -engine tencent input.tex -o output.tex`. You can also permanently change the settings through `translate_tex --setdefault`. You can view more details through `translate_tex --help`. `translate_arxiv` also provides exactly the same command line arguments, which have the same effect.

If you have any questions or have interests in making contributions, please contact me by susyustc@gmail.com or joining QQ group 288646946.

## Custom commands
During the translation process, you may encounter that some content is not translated, which is generally caused by some custom commands that have not been recognized. In the command line mode, we provide the function of custom commands, you only need to create a file (such as `MT_additional_commands.txt`), which defines the commands that need to be translated, for example:
```
# if you need more, just add lines with the same format (don't miss the ","!)
# each line is in the format of (command_name, N, (n1, n2, ...)),
# N is the total number of arguments,
# n1, n2, ... are the index of arguments requiring translation (counting from 0)
additional_commands = [
   # latex: \mycommand1{translation needed}
   ('mycommand1', 1, (0, )),
   # latex: \mycommand2{translation not needed}{translation needed}
   ('mycommand2', 2, (1, )),
   # latex: \mycommand3{translation needed}{translation not needed}
   ('mycommand3', 2, (0, )),
   # latex: \mycommand4{translation needed}{translation not needed}{translation needed}{translation not needed}
   ('mycommand4', 4, (0, 2)),
   # practical example: \textcolor{red}{Need translation here}
   ('textcolor', 2, (1, )),
]
```
Then add command line parameters `-commands MT_additional_commands.txt` to translate custom commands.

## Donation
If you think this project is helping you a lot, you can support us by the Wechat QR code below
<p align="center">
  <img width=30% src="https://github.com/SUSYUSTC/MathTranslate/assets/30529122/16f82637-e102-4330-82ad-bbcbdad1c19d">
</p>
