#!/usr/bin/env python

import os
import trie
from time import sleep

# CONTROL COMMAND
SPACE      = 27
REPEAT     = 28
BACKASPACE = 29
RESET      = 30
COMMIT     = 31

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pindex = 0
word = ""

map = " abcdefghijklmnopqrstuvwxyz"
trie = trie.Trie()
f = open("words.txt", "r")
for line in f:
    line = line[:len(line)-2]
    #print(line, ", ", line.isalpha())
    trie.add(line)

while True:
    cindex = 0
    if (GPIO.input(27) == True):
        cindex += 16
    if (GPIO.input(26) == True):
        cindex += 8
    if (GPIO.input(25) == True):
        cindex += 4
    if (GPIO.input(24) == True):
        cindex += 2
    if (GPIO.input(23) == True):
        cindex += 1

    if (cindex == 0 and pindex != 0):
        if (pindex == 31):
            #print(word)
            if (trie.has_word(word)):
                os.system('./test_speech.sh ' + word)
            word = ""
	elif (pindex == 30):
	    word = ""
	elif (pindex == 29):
	    word = word[:len(word)-1]
	    #print word
        else:
            word += map[pindex]
            #print ('Letter', map[pindex])
	    #print word
	print word
    pindex = cindex

    sleep(0.5)



