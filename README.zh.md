# MathTranslate
[![zh](https://img.shields.io/badge/lang-zh-yellow.svg)](https://github.com/SUSYUSTC/MathTranslate/main/README.md)

这是一个将带有大量数学符号的论文，在保持数学公式与符号不变的前提下，从任何语言翻译成任何语言的项目。在大多数翻译软件中，您无法保留公式，这会让您很苦恼。
该项目基于以下两个工具：
1. mathpix: 提供了一个将text+equation图片转换成latex代码的接口。
2. translate-shell: 提供google translate的终端界面

该项目的主要工作是将LaTex文件从一种语言翻译成另一种语言，并提供一个将它们组合起来的界面。

这里有一个示例：
<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/225237425-9341b03e-25b5-4617-b606-5e3813de3ec2.png" width="260">
<img src="https://user-images.githubusercontent.com/30529122/225234174-78af1e5f-aeff-4dd8-9f4c-d948edc35318.png" width="400">
</p>

## 安装需求
1. 一个带有OCR的mathpix账号 https://mathpix.com/docs/ocr/overview
2. 带有`requests`库的python 3：可以通过`pip install requests`安装
3. translate-shell: 可以通过`sudo apt-get install translate-shell`安装
4. texlive (或者任何一个可以从tex生成pdf的工具): 可以通过`sudo apt-get install texlive-full`安装

## 使用
1. 在 `MathTranslate/scripts/mpix.py` 中，将 'YOUR_APP_ID' 和 'YOUR_APP_KEY' 替换为您从 mathpix 网站获得的 OCR ID 和密钥（速率限制为每分钟 200 次，这已经足够了，除非您想翻译大批量文档）
2. 添加目录 `MathTranslate/scripts` 到 PATH
3. 将论文的各个部分逐个截图，并在你的目录下以part1.png,part2.png,...partXXX.png命名，如下图所示。基本上每个屏幕截图都是半页/一页，具体取决于纸张布局，您只需要避免包含数字即可。（在后续更新中我们将尽量避免截图，优化使用流程）
<img src="https://user-images.githubusercontent.com/30529122/225232807-88c1dba4-f513-4688-9c6c-6dc7fa708cda.png" width="500">

4. 在此文件夹中运行“translate.sh”，然后“main.pdf”（和“main.tex”）就是你所需要的！
5. 由于本项目较小，有时需要对最终的tex文件稍作改动进行编译。
6. 默认代码是将英文翻译成中文。如果你想从/翻译成其他语言，你只需要在 `MathTranslate/scripts/translate_tex.py` 中更改 `language_from` 和 `language_to`

## 特点
1. 如果您的截图图片顺序正确，按页/图分割的段落将自动连接
2. mathpix生成操作（比较耗时）被缓存。这意味着如果您只添加 1 个额外的屏幕截图，则不必再次运行所有内容。您可以一开始只尝试 1-2 个，然后再决定是否添加更多。

## 例子
在示例目录中，运行 `translate.sh`，您会获得与 `main.tex` 和 `main.pdf` 相同的结果。
