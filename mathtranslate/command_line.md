# 🏗️ Command line Usage


## Backend engine
The default engine is google translate, which can not be accessed with IP in mainland China. For users with IP in mainland China we provide the tencent engine, although its accuracy is not as good as the google engine. 
To use the tencent engine, you need to register the [Tencent Translation API](https://cloud.tencent.com/product/tmt) account. After registration, you can get the secret ID (not the APP ID!) and secret Key in [Tencent Console](https://console.cloud.tencent.com/cam/capi). Tencent Translate is the translation API with the highest free quota to our knowledge besides Google Translate, with a free quota of 5 million characters per month, and no fee will be deducted if there is no manual recharge (that is, there is no need to worry about misuse).

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
