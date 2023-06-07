#!/bin/bash
for filename in be caption brace accent
do
    translate_tex ./input_${filename}.tex -o ./output_${filename}.tex --nocache
    diff ./output_${filename}.tex ./ref_${filename}.tex
    cat ./output_${filename}.tex
done
