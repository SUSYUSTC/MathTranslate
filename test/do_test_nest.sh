#!/bin/bash
translate_tex test_nest.txt
diff test_nest.tex test_nest_ref.tex
rm -f test_nest.tex
