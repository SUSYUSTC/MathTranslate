#!/bin/bash
filename=$1
translate_tex ./input_${filename}.tex -o ./output_${filename}.tex --nocache
difference=$(diff ./output_${filename}.tex ./ref_${filename}.tex)
if [ "$difference" == "" ]; then
    echo -e "\033[0;31m Good \033[0m"
else
    echo -e "\033[0;31m Bad \033[0m"
    echo begin difference
    echo $difference
    echo end difference
fi
cat ./output_${filename}.tex
