#!/bin/bash
function echoline(){
	for i in $@
	do
		echo $i
	done
}
function sortN(){
	echoline $@ | sort -V
}

# generate latex for each screenshot in the original language by mathpix OCR
for file in part*.png
do
    filename="${file%.*}"
    if [ ! -f $filename.txt ]; then
        mpix.py $filename.png > $filename.txt
        echo $filename.png converted
    else
        echo $filename.png cached
    fi
done

# combine them to a single latex file
rm -f main.txt
for file in $(sortN part*.txt)
do
    cat $file >> main.txt
done

# the translate the latex file while keeping math symbols and equations
translate_txt.py main.txt main.tex

# compile latex to pdf
pdflatex main.tex
