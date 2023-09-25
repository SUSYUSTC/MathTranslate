# 👀 GUI 

https://github.com/SUSYUSTC/MathTranslate/assets/30529122/04c1971d-b094-41d8-bdbb-6dd65d4b81c4


## GUI usage

Simply [download](https://github.com/SUSYUSTC/MathTranslate/releases) the corresponding executable file and you are done!

You can set the translation engine and language in the **Preference** page. If you plan to use the tencent engine, you need to set the secret ID and secret Key.
1. If you want to translate a paper on [arxiv](https://arxiv.org/), you can use the **Arxiv Translate** function. You just need to enter the arxiv number of the paper you want to translate (for example 2205.15510). After the translation you will get a `.zip` file, which contains the latex source code of the arxiv project.
2. If you want to translate a paper only with pdf version, you can first convert the pdf to latex by [mathpix](https://mathpix.com/) and then use the **File Translate** function. Unfortunately, mathpix requires a fee after exceeding a certain amount of usage. Here is the [price list](https://mathpix.com/pricing). After the translation you will get a `.tex` file which contains the corresponding latex file.

After the translation is done you can upload either the `.zip` (New Project - Upload Project) or `.tex` (New Project - Blank Project and copy-paste) file to [overleaf](https://www.overleaf.com/project) for online compilation.
**Note: you have to set the compiler to XeLatex in `Menu - Compiler`.**


## GUI 使用

只需[下载](https://github.com/SUSYUSTC/MathTranslate/releases)相应的可执行文件即可完成！

您可以在 **Preferences** 页面中设置翻译引擎和语言。如果您打算使用腾讯翻译引擎，您需要设置 secret ID 和secret Key。
1. 如果您想翻译 [arxiv](https://arxiv.org/) 上的论文，可以使用 **Arxiv Translate** 功能。 您只需输入要翻译的论文的 arxiv 编号（例如2205.15510）。翻译后你会得到一个 `.zip` 文件，其中包含 arxiv 项目的 latex 源代码。
2. 如果您想翻译仅有 pdf 版本的论文，可以先通过 [mathpix](https://mathpix.com/) 将 pdf 转换为 latex ，然后使用**文件翻译**功能。 不幸的是， mathpix 在超过一定的使用量后需要付费。 这是[价格表](https://mathpix.com/pricing)。 翻译后您将得到一个 `.tex` 文件。

翻译完成后，您可以将 `.zip`（New Project - Upload Project）或 `.tex`（New Project - Blank Project 然后复制粘贴）文件上传到 [overleaf](https://www.overleaf.com/project)在线编译。
**注意：您必须在 `Menu - Compiler` 中将编译器设置为 XeLatex**。