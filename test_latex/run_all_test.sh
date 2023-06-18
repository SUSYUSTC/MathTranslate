#!/bin/bash
for filename in be caption brace accent mularg bibnote
do
    ./run_single_test.sh $filename
done
