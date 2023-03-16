# MathTranslate
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.md)
[![zh](https://img.shields.io/badge/lang-zh-yellow.svg)](https://github.com/SUSYUSTC/MathTranslate/blob/main/README.zh.md)

<p align="center">
  <a href="https://github.com/SUSYUSTC/MathTranslate">
    <img width=30% src="logo_zh.jpg">
  </a>
</p>


大多数翻译软件无法很好地处理论文中的数学公式，许多科研工作者为此饱受困扰。本项目可以将含有大量数学公式的科研论文在任何语言之间翻译。
该项目基于以下两个工具：
1. [mathpix](https://mathpix.com/): 提供了一个将 text+equation 图片转换成 latex 代码的接口。不幸的是它不是完全免费的，价格可以在 https://mathpix.com/pricing 查看。在后续开发中我们会尽量减少需要的使用次数以节省您的开支。（我们的软件本身是完全免费开源的！）
2. [translate-shell](https://github.com/soimort/translate-shell): 提供 google translate 的终端界面。

该项目的主要工作是将 LaTex 文件从一种语言翻译成另一种语言，并提供一个将以上两个工具组合起来的界面。

这里是示例：
<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/225237425-9341b03e-25b5-4617-b606-5e3813de3ec2.png" width="260">
<img src="https://user-images.githubusercontent.com/30529122/225234174-78af1e5f-aeff-4dd8-9f4c-d948edc35318.png" width="400">
</p>

虽然它目前是一个小项目，但我们知道这个项目受到的关注比我们预期的要多得多。 我们正在计划更多的开发，以获得更好的用户体验。

## 发布
### 2023年3月16日
我们已经完成了对各操作系统的兼容。只需要 python 和 pip 就能完成所有的操作。

## 安装需求
1. 一个 [mathpix](https://mathpix.com/) 帐户。 不幸的是，它不是完全免费的。目前 mathpix 免费提供 100 个截图（注册时需要一封edu电子邮件）或者以每月 5 美元的价格提供 5000 个截图。
2. Python3 和 [mtranslate](https://pypi.org/project/mtranslate) 包: `pip install mtranslate`
3. texlive (或者任何可以从tex生成pdf的工具)

## 使用
1. 下载 mathpix 。 在 Settings-Formatting 中，将“Inline math delimiters”和“Block mode delimiters”分别改为“\\( ... \\)”和“\\[ ... \\]”。
 <img src="https://user-images.githubusercontent.com/30529122/225747242-07b89c34-4f16-40f9-bebc-d0c0b1c4c8e8.png" width="600">
 
2. 添加目录 `MathTranslate/scripts` 到 PATH。
3. 用 mathpix 把你要翻译的内容截图，复制输出的 latex 代码，保存到 txt 文件中。假设文件名为 `main.txt`。mathpix 目前可以识别连贯的文字（可以是一段或多段）。您也可以连续截图-复制多段分隔开的文字放在同一个 txt 文件中，我们在下一步的翻译中会自动识别与合并被图片或者分页隔开的段落。
4. 在此文件夹中运行 `translate_tex.py main.txt`。 您将获得一个翻译后的 tex 文件 `main.tex`，如果您的机器上安装了`xelatex`的话也会同时生成 pdf 文件。
5. 由于本项目较小，有时需要对最终的 tex 文件稍作改动进行编译。
6. 默认代码是将英文翻译成中文。如果你更改任意一端的语言，你只需要在 `MathTranslate/scripts/translate_tex.py` 中更改 `language_from` 和 `language_to`即可。

## 例子
在示例目录中，您可以看到 `main.txt`，它是最近一篇论文的一部分的 mathpix 输出。 运行 `translate_tex.py main.txt`，您会获得 `main.tex` 和 `main.pdf` 。

## 进一步开发
1. 自动从pdf中提取图片，批量处理图片，一键输出整个翻译好的pdf！
2. 通过开源软件减少 mathpix 的请求次数。
3. 简化用户界面。

如果您有兴趣做出贡献，请通过 susyustc@gmail.com 与我联系或加我微信号 sunjiace2262。
