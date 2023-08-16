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
    <img src="https://img.shields.io/badge/GUI-v3.0.2-red.svg?logo=apache"/>
  </a>
</p>


<p align="center">
  <a href="https://github.com/SUSYUSTC/MathTranslate">
    <img width=30% src="logo_zh.jpg">
  </a>
</p>

<p align="center"> <a href="README.md">English</a> |  简体中文 </p>

<p align="center"> <a href="https://github.com/SUSYUSTC/MathTranslate/releases"> GUI 下载地址 </a></p>


大多数翻译软件无法很好地处理论文中的数学公式，许多科研工作者为此饱受困扰。本项目可以将含有大量数学公式的科研论文在任何语言之间翻译。

该项目的主要工作是基于纯文字的谷歌翻译实现 LaTeX 文件的翻译，从而最终实现 pdf 的翻译。

这里是示例:

<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/227698548-1cc19f7c-00e7-4312-9d58-2a7237656b51.png" width="700">
</p>

<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

## 发布
### 2023年6月24日
我们发布了 MathTranslate 的 [GUI](https://github.com/SUSYUSTC/MathTranslate/releases)。 无需任何额外安装，直接使用即可！
### 2023年5月14日
增加了一键翻译完成 arxiv 项目的功能。
### 2023年3月24日
增加了直接翻译 arxiv 论文的功能。
### 2023年3月21日
对IP地址在中国大陆的用户，我们增加了腾讯翻译的选项。
### 2023年3月16日
我们已经完成了对各操作系统的兼容。现在只需要 `pip install --upgrade mathtranslate` 就可以完成安装。

## 后端引擎
默认引擎是 google 翻译，中国大陆IP无法访问。 对于中国大陆IP的用户，我们提供腾讯引擎，虽然其准确性不如 google 引擎。
使用腾讯引擎需要注册 [腾讯翻译API](https://cloud.tencent.com/product/tmt)账号。 注册后，您可以在[腾讯控制台](https://console.cloud.tencent.com/cam/capi)中获取secret ID（不是APP ID！）和secret Key。 腾讯翻译是据我们所知除谷歌翻译外免费额度最高的翻译API，每月有500万字符免费额度，且不手动充值情况下不会扣费（即不用担心误操作）。

## 代理设置
如果您打算通过设置代理的方式使用 google 引擎，可能需要设置环境变量，否则在浏览器以外的情况下代理可能无效。需要设置的环境变量为`http_proxy`和`https_proxy`，例如
```
export http_proxy=http://127.0.0.1:7890
export https_proxy=https://127.0.0.1:7890
```
其中的代理地址和端口会根据不同代理软件有所不同。Windows 中也可以通过非命令行的方式设置环境变量。

## GUI 安装
只需[下载](https://github.com/SUSYUSTC/MathTranslate/releases)相应的可执行文件即可完成！

## GUI 使用

https://github.com/SUSYUSTC/MathTranslate/assets/30529122/04c1971d-b094-41d8-bdbb-6dd65d4b81c4

您可以在 **Preferences** 页面中设置翻译引擎和语言。如果您打算使用腾讯翻译引擎，您需要设置 secret ID 和secret Key。
1. 如果您想翻译 [arxiv](https://arxiv.org/) 上的论文，可以使用 **Arxiv Translate** 功能。 您只需输入要翻译的论文的 arxiv 编号（例如2205.15510）。翻译后你会得到一个 `.zip` 文件，其中包含 arxiv 项目的 latex 源代码。
2. 如果您想翻译仅有 pdf 版本的论文，可以先通过 [mathpix](https://mathpix.com/) 将 pdf 转换为 latex ，然后使用**文件翻译**功能。 不幸的是， mathpix 在超过一定的使用量后需要付费。 这是[价格表](https://mathpix.com/pricing)。 翻译后您将得到一个 `.tex` 文件。

翻译完成后，您可以将 `.zip`（New Project - Upload Project）或 `.tex`（New Project - Blank Project 然后复制粘贴）文件上传到 [overleaf](https://www.overleaf.com/project)在线编译。
**注意：您必须在 `Menu - Compiler` 中将编译器设置为 XeLatex**。

## 命令行安装
1. 安装 Python3 和 pip。
2. `pip install --upgrade mathtranslate`

## 命令行使用
**对于 Windows 用户，您可能需要以管理员身份运行 cmd 或 powershell 。**
1. 准备或生成一个 tex 文件或项目。你可以用如下方式得到 tex 文件或项目：
    - 对于大多数 [arxiv](https://arxiv.org/) 论文， latex 源代码是公开的。对于 arxiv 论文，我们提供了一个简单 API 从 arxiv number 一键翻译整个项目。
    - 使用 [mathpix](https://mathpix.com/) 把你想翻译的 pdf 转成 latex 代码。mathpix 可以直接把 pdf 或截图转换成 latex 代码，这两种方式我们都可以处理。不幸的是，mathpix 在使用超过一定数量之后需要收费，这里是[价格表](https://mathpix.com/pricing)。
2. （腾讯翻译API用户）运行`translate_tex --setkey`来存储 API secretID 和 secretKey。
3. 使用命令行翻译　tex 文件或项目
   - 翻译单个文件: `translate_tex input.tex -o output.tex` 会生成翻译后的 tex 文件 `output.tex`。
   - 翻译 arxiv 项目: `translate_arxiv 2205.15510` 会生成翻译后的 tex 项目 `2205.15510.zip`。
4. 编译您的 tex 文件。对于单个文件，您可以用 [texlive](https://www.tug.org/texlive/) 的命令 `xelatex output.tex` 编译。中文翻译需要 xeCJK 包。对于 arxiv 项目我们建议把得到的 .zip 文件上传到 overleaf 在线编译 (New Project - Upload Project)。**注意，您需要在 `Menu - Compiler` 中设置成 XeLatex 编译器。**
5. 您可以通过命令行参数 `-engine`、`-from`、`-to` 更改翻译语言和引擎的默认设置。 例如 `translate_tex -engine tencent input.tex -o output.tex`。 您还可以通过 `translate_tex --setdefault` 永久更改设置。 您可以通过 `translate_tex --help` 查看更多细节。`translate_arxiv`也提供完全相同的命令行参数，它们的效果是一样的。

如果您有任何问题或有兴趣做出贡献，请通过 susyustc@gmail.com 与我联系或加入 QQ 群 288646946 。

## 自定义命令
在翻译过程中您可能会遇到一些内容没有被翻译出来，这一般是因为有一些自定义的命令没有被识别到导致的。在命令行模式中我们提供了自定义命令的功能，您只需创建一个文件（例如`MT_additional_commands.txt`），里面定义需要翻译的命令，例如：
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
之后加上命令行参数 `-commands MT_additional_commands.txt` 即可翻译自定义的命令。

## 捐赠
如果您觉得本软件对您非常有帮助，可以通过下面的二维码向我们捐赠
<p align="center">
  <img width=30% src="https://github.com/SUSYUSTC/MathTranslate/assets/30529122/16f82637-e102-4330-82ad-bbcbdad1c19d">
</p>
