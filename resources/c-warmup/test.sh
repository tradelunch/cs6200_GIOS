#!/usr/bin/env bash

input="input.txt"
output="output.txt"

rm -f ${input} ${output}

./generate-input.py > ${input}
./sum-input ${input} ${output}
./validate.py ${input} ${output}

if [ $? -eq 0 ];
then
    echo "Your code passed the test :)"
else
    echo "Your code did not pass the test :("
fi
