import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_text_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


here = os.path.abspath(os.path.dirname(__file__))
version = read_text_file(os.path.join(here, "mathtranslate", "version.txt"))
author = read_text_file(os.path.join(here, "mathtranslate", "author.txt"))

setuptools.setup(
    name="mathtranslate",
    version=version,
    author=author,
    author_email="susyustc@gmail.com",
    description="Translate math-heavy papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SUSYUSTC/MathTranslate",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["mtranslate",
                      "charset-normalizer",
                      "requests",
                      "regex",
                      "tqdm",
                      "appdata"
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'translate_tex=mathtranslate.translate_tex:main',
            'translate_arxiv=mathtranslate.translate_arxiv:main',
        ]
    },
)
