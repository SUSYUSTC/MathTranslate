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
该项目基于以下两个工具：
1. [mathpix](https://mathpix.com/): 提供了一个将 text+equation 图片转换成 latex 代码的接口。不幸的是它不是完全免费的，价格可以在 https://mathpix.com/pricing 查看。在后续开发中我们会尽量减少需要的使用次数以节省您的开支。（我们的软件本身是完全免费开源的！）
2. 谷歌翻译。

该项目的主要工作是基于纯文字的谷歌翻译实现 LaTex 文件的翻译，并结合 mathpix 最终实现 pdf（或其他格式） 到 pdf 的翻译。

这里是示例：
<p float="left">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/screenshot.png" width="300">
<img src="https://github.com/SUSYUSTC/MathTranslate/blob/main/example/translated.png" width="400">
</p>

虽然它目前是一个小项目，但我们知道这个项目受到的关注比我们预期的要多得多。 我们正在计划更多的开发，以获得更好的用户体验。

## 发布
### 2023年3月22日
修复了一些主要的bug。
### 2023年3月21日
对IP地址在中国大陆的用户，我们增加了腾讯翻译的选项。
### 2023年3月16日
我们已经完成了对各操作系统的兼容。现在只需要 `pip install --upgrade mathtranslate` 就可以完成安装。

## 安装需求
1. 一个 [mathpix](https://mathpix.com/) 帐户。 不幸的是，它不是完全免费的。目前 mathpix 免费提供 100 个截图（注册时需要一封edu电子邮件）或者以每月 5 美元的价格提供 5000 个截图。
2. Python3 和 pip。建议使用 [Anaconda](https://www.anaconda.com)。
3. texlive (或者任何可以从tex生成pdf的工具)，中文输出需要 CJK 包。
4. （中国大陆IP用户）：一个 [腾讯翻译 API](https://cloud.tencent.com/product/tmt) 帐户。 注册后可以在 [腾讯控制台](https://console.cloud.tencent.com/cam/capi) 获取 secret ID 和 secret key 。 腾讯翻译是除谷歌翻译之外我们认知范围内免费额度最高的翻译 API，每月有500万字符免费额度，且不手动充值情况下不会扣费（即不用担心误操作）。

## 安装
`pip install --upgrade mathtranslate`

## 使用
1. 下载 mathpix。
2. （腾讯翻译API用户）运行`translate_tex --setkey`来存储API ID和key。
3. 用 mathpix 把你要翻译的内容截图，复制输出的 latex 代码，保存到 txt 文件中。mathpix 目前可以识别连贯的文字（可以是一段或多段）。您也可以连续截图-复制多段分隔开的文字放在同一个 txt 文件中，我们在下一步的翻译中会自动识别与合并被图片或者分页隔开的段落。
4. 假设您上一步保存的文件名为 `main.txt`。在此文件夹中运行 `translate_tex main.txt`。 您将获得一个翻译后的 tex 文件 `main.tex`，如果您的机器上安装了`xelatex`的话也会同时生成 pdf 文件。
5. 由于本项目较小，有时需要对最终的 tex 文件稍作改动进行编译。
6. 您可以通过命令行参数“-engine”、“-from”、“-to”更改翻译语言和引擎的默认设置。 例如 `translate_tex -engine tencent main.txt`。 您还可以通过 `translate_tex --setdefault` 永久更改设置。 您可以通过 `translate_tex --help` 查看更多细节。

## 例子
在示例目录中，您可以看到 `main.txt`，它是 `paper.pdf` 的一部分的 mathpix 输出。 运行 `translate_tex main.txt`，您会获得 `main.tex` 和 `main.pdf` 。`translated.png` 是你在 `main.pdf` 里预期会看到的内容。

## 进一步开发
1. 自动从pdf中提取图片，批量处理图片，一键输出整个翻译好的pdf！
2. 通过开源软件减少 mathpix 的请求次数。
3. 简化用户界面。

如果您有任何问题或有兴趣做出贡献，请通过 susyustc@gmail.com 与我联系或加入 QQ 群 288646946 。
