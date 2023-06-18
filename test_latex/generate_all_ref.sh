#!/bin/bash
for filename in be caption brace accent mularg bibnote
do
    ./generate_single_ref.sh $filename
done
