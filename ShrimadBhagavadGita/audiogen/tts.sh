#!/bin/bash

python3 vertexspeech.py
cloudshell download zvertex_ai_audio.wav 
cat input.txt >> all_input.txt
echo >> all_input.txt

