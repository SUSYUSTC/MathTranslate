Requirements:
A mathpix account with OCR
https://mathpix.com/docs/ocr/overview
python 3 with libraries: pip install requests
translate-shell: sudo apt-get install translate-shell
texlive (or any other tool to generate pdf from tex): sudo apt-get install texlive-full

Usage:
1. In mpix.py, replace 'YOUR_APP_ID' and 'YOUR_APP_KEY' with the OCR ID and key you get from mathpix website (the rate limit is 200 times per minute which is more than enough unless you want to translate a huge batch)
2. Add this directory to $PATH
3. Screenshot each part of your paper one by one and name them by part1.png, part2.png, ... partXXX.png in some folder.
4. Run "translate.sh" in this folder then 'main.pdf' is all you need!
5. Since this project is small, sometimes you need to slightly change the final tex file for compilation.

Examples
In the directory examples, run "translate.sh" and you would expect to get the same with 'main.tex' and 'main.pdf'.
