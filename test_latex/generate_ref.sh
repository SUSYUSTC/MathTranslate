#!/bin/bash
for filename in be caption brace accent mularg
do
    translate_tex ./input_${filename}.tex -o ./ref_${filename}.tex --nocache
done
