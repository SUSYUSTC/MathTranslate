pyi-makespec --onefile --noconsole --add-data ./guipage/page.kv:./guipage --add-data ./guipage/dialog.kv:./guipage --add-data ./guipage/preferencespage.kv:./guipage MathTranslate.py
pyinstaller MathTranslate.spec
