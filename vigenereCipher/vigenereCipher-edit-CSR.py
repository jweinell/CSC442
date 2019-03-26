#!/usr/bin/python

import sys
ARGUMENTS = sys.argv
OPTION = ARGUMENTS[1]
KEY = ARGUMENTS[2]

def keySetup(key, options):
    key = "".join(key.lower().split())
    keyarray = []
    for letter in key:
        if (options == "-e"):
            keyarray.append(ord(letter) - 97)
        elif (options == "-d"):
            keyarray.append(26 - (ord(letter) - 97))
        else:
        	print "Error: Unknown option {}".format(options)
        	sys.exit()
    return keyarray

def encode(sometext, key):
    encoded = ""
    index = 0
    for character in sometext:
        if character.isalpha():
            if character.isupper():
                base = 65
            else:
                base = 97
            charnum = ((ord(character) - base + key[index%len(key)])%26) + base
            newcharacter = chr(charnum)
            index = index + 1
        else:
            newcharacter = character
        encoded = encoded + newcharacter
    print encoded

while(1):
	INPUT_STR = sys.stdin.readline().strip()
	if (INPUT_STR == ""):
		break
	encoded_key = keySetup(str(KEY), OPTION)
	encode(INPUT_STR, encoded_key)
