#!/bin/bash
filename=$1
translate_tex ./input_${filename}.tex -o ./ref_${filename}.tex --nocache
