 
#!/usr/bin/env python

import sys
import os
import trie
from time import sleep
import RPi.GPIO as GPIO
from socket import *
import socket
from time import ctime
from subprocess import check_output

# Client information
PORT = 1200
BUFSIZE = 1024
MOBILE_IP = "192.168.100.58"

# CONTROL COMMAND
SPACE      = 27
REPEAT     = 28
BACKSPACE  = 29
RESET      = 30
COMMIT     = 31

# ALL BUTTONS
BUTTON_5 = 27
BUTTON_4 = 26
BUTTON_3 = 25
BUTTON_2 = 24
BUTTON_1 = 23

print "Text to speech - application"
print "Raspberry 3"
print ""

ip_two = check_output(['hostname', '-I'])
ip = ip_two.split(' ')[1]
print "IP Address of Raspbbery PI:   " + ip

# Datagram (UDP) socket - client
#___client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#___client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#___client.sendto(ip, (BROADCAST, PORT))
#___print "Waiting data from server ..."

#___f = client.makefile('rb')
#___data = f.read(1024)
#___MOBILE_IP, ADDR_1 = client.recvfrom(BUFSIZE)
#___print 'Data received !'
#___print "IP address of Mobile device: " + data
#___client.close()

#___MOBILE_IP = "192.168.100.58"
#___print "Connect RPi with Mobile device "
#___client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#___client.connect((MOBILE_IP, PORT));
#___print 'TCP client started on Raspberry PI with server on Mobile device.'

#___MOBILE_IP, ADDR_1 = client.recvfrom(BUFSIZE)
#___print "IP address of Mobile device: " + MOBILE_IP

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
	    #___client.send(sentence + "\n")
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

    sleep(0.3)

client.close()
print "TCP client closed. "
