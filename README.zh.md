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
    <img width=30% src="logo_zh.jpg">
  </a>
</p>

<p align="center"> <a href="README.md">English</a> |  简体中文 </p>

大多数翻译软件无法很好地处理论文中的数学公式，许多科研工作者为此饱受困扰。本项目可以将含有大量数学公式的科研论文在任何语言之间翻译。

该项目的主要工作是基于纯文字的谷歌翻译实现 LaTex 文件的翻译，从而最终实现 pdf 的翻译。

这里是示例:

<p float="left">
<img src="https://user-images.githubusercontent.com/30529122/227698548-1cc19f7c-00e7-4312-9d58-2a7237656b51.png" width="700">
</p>

<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

虽然它目前是一个小项目，但我们知道这个项目受到的关注比我们预期的要多得多。 我们正在计划更多的开发，以获得更好的用户体验。

## 发布
### 2023年3月24日
增加了直接翻译 arxiv 论文的功能。
### 2023年3月21日
对IP地址在中国大陆的用户，我们增加了腾讯翻译的选项。
### 2023年3月16日
我们已经完成了对各操作系统的兼容。现在只需要 `pip install --upgrade mathtranslate` 就可以完成安装。

## 安装需求
1. Python3 和 pip。建议使用 [Anaconda](https://www.anaconda.com)。
2. （中国大陆IP用户）： [腾讯翻译 API](https://cloud.tencent.com/product/tmt) 帐户。 注册后可以在 [腾讯控制台](https://console.cloud.tencent.com/cam/capi) 获取 secret ID 和 secret key 。 腾讯翻译是除谷歌翻译之外我们认知范围内免费额度最高的翻译 API，每月有500万字符免费额度，且不手动充值情况下不会扣费（即不用担心误操作）。

## 安装与更新
`pip install --upgrade mathtranslate -i https://pypi.org/simple`

**我们建议用户在使用前始终检查更新，因为我们更新地比较频繁**

## 使用
1. 准备或生成一个 tex 文件。你可以用如下方式得到 tex 文件：
    - 对于大多数 [arxiv](https://arxiv.org/) 论文，你可以下载到 latex 源代码 (Download - Other formats - Source)。如果你下载得到的文件没有后缀，大部分情况下是 .tar 格式，您可能需要手动加上后缀。解压后你可以得到一个 latex 项目，然后你可以翻译其中的 .tex 文件。
    - 使用 [mathpix](https://mathpix.com/) 对你想翻译的部分截图。你可以一次性截图连着的一大片（甚至可以直接截图一整页，如果没有图片的话），并且可以多次截图的 Latex 代码合成成一个文件。不幸的是，它不是完全免费的。目前 mathpix 免费提供 100 个截图（注册时需要一封edu电子邮件）或者以每月 5 美元的价格提供 5000 个截图。
2. （腾讯翻译API用户）运行`translate_tex --setkey`来存储 API ID 和 key。
3. 通过 `translate_tex input.tex -o output.tex` 翻译 tex 文件。
4. 编译您的 tex 文件。您可以用 [texlive](https://www.tug.org/texlive/) 的命令 `xelatex output.tex` 编译。中文翻译需要 xeCJK 包。如果是下载的 arxiv 项目我们建议把所有文件压缩成 zip 文件后上传到 [overleaf](https://www.overleaf.com/project) 在线编译。**注意，您需要在 `Menu - Compiler` 中设置成 XeLatex 编译器，否则无法处理其他语言。**
5. 您可以通过命令行参数 `-engine`、`-from`、`-to` 更改翻译语言和引擎的默认设置。 例如 `translate_tex -engine tencent input.tex -o output.tex`。 您还可以通过 `translate_tex --setdefault` 永久更改设置。 您可以通过 `translate_tex --help` 查看更多细节。

## 例子
在示例目录中，您可以看到 `main.txt`，它是 `paper.pdf` 的一部分的 mathpix 输出。 运行 `translate_tex main.txt`，您会获得 `main.tex` 和 `main.pdf` 。`translated.png` 是你在 `main.pdf` 里预期会看到的内容。

## 已知的问题
1. 如果 latex 中用 `\newcommand` 重新设置了 `\begin{env} \end{env}` 会无法正确翻译。
2. 翻译时会有一个很小的概率产生类似 "XMATHX_1_2" 的代码或公式错误。腾讯翻译正确率会比谷歌翻译略低一些。

## 进一步开发
1. 解决 Latex 翻译的 bug。
2. 简化用户界面。

如果您有任何问题或有兴趣做出贡献，请通过 susyustc@gmail.com 与我联系或加入 QQ 群 288646946 。
