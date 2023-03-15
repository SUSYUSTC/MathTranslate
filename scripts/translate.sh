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
for file in part*.png
do
    filename="${file%.*}"
    if [ ! -f $filename.tex ]; then
        mpix.py $filename.png > $filename.tex
        echo $filename.png converted
    else
        echo $filename.png cached
    fi
done
rm -f old.tex
for file in $(sortN part*.tex)
do
    cat $file >> old.tex
done
translate_tex.py old.tex main.tex
xelatex main.tex
