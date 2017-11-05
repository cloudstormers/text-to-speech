#!/usr/bin/env python

import os
import trie
from time import sleep
import RPi.GPIO as GPIO

# CONTROL COMMAND
SPACE      = 27
REPEAT     = 28
BACKSPACE  = 29
RESET      = 30
COMMIT     = 31

BUTTON_5 = 27
BUTTON_4 = 26
BUTTON_3 = 25
BUTTON_2 = 24
BUTTON_1 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pindex = 0
sentence = ""
word = ""
map = " abcdefghijklmnopqrstuvwxyz"

trie = trie.Trie()
f = open("words.txt", "r")
for line in f:
    line = line[:len(line)-2]
    trie.add(line)

while True:
    cindex = 0
    if (GPIO.input(BUTTON_5) == True):
        cindex += 16
    if (GPIO.input(BUTTON_4) == True):
        cindex += 8
    if (GPIO.input(BUTTON_3) == True):
        cindex += 4
    if (GPIO.input(BUTTON_2) == True):
        cindex += 2
    if (GPIO.input(BUTTON_1) == True):
        cindex += 1

    if (cindex == 0 and pindex != 0):
        if (pindex == COMMIT):
            os.system('./test_speech.sh ' + sentence)
            sentence = ""
        elif (pindex == SPACE):
            if (trie.has_word(word)):
                if (sentence == ""):
                    sentence += word
                else:
                    sentence += " " + word
            word = ""
        elif (pindex == RESET):
            word = ""
        elif (pindex == REPEAT):
            sentence += " " + sentence + " " + sentence 
        elif (pindex == BACKSPACE):
            word = word[:len(word) - 1]
        elif (1 <= pindex <= 26):
            word += map[pindex]
        print(sentence + "-" + word)
    pindex = cindex

    sleep(0.2)



