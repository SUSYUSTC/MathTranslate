rm -rf build
pyi-makespec --onefile --noconsole --add-data ./guipage/page.kv:./guipage --add-data ./guipage/dialog.kv:./guipage --add-data ./guipage/preferencespage.kv:./guipage --add-data ./yahei.ttf:./ MathTranslate.py
pyinstaller MathTranslate.spec

rm -rf build
pyi-makespec --onefile update.py
pyinstaller update.spec
