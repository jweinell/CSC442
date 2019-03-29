#!/usr/bin/python
# Github for Team: https://github.com/jweinell/CSC442/
# It's a private repository, FYI -- jweinell can grant you access

import sys
ARGUMENTS = sys.argv
# verify inputs exists and respond accordingly if needed
try:
    OPTION = ARGUMENTS[1]
    KEY = ARGUMENTS[2]
except IndexError:
    print "usage: \n" + sys.argv[0] + " -e|-d key"
    exit()

# returns an array to be looped over to shift the input_data
def keySetup(key, options):
    # remove white space from key and make lower case
    key = "".join(key.lower().split())
    keyarray = []
    for letter in key:
        # each letter of the key shifts differently depending
        # on whether we are encoding or decoding
        if (options == "-e"):
            keyarray.append(ord(letter) - 97)
        elif (options == "-d"):
            keyarray.append(26 - (ord(letter) - 97))
        else:
        	print "Error: Unknown option {}".format(options)
        	sys.exit()
    return keyarray

# takes a string to enclode/decode as input along with an int
# array to shift the text
def encode(sometext, key):
    encoded = ""
    index = 0
    for character in sometext:
        # characters are shifted differently based on whether they are
        # upper or lower case
        if character.isalpha():
            if character.isupper():
                base = 65
            else:
                base = 97
            # calculate the int value of the new character
            charnum = ((ord(character) - base + key[index%len(key)])%26) + base
            newcharacter = chr(charnum)
            index = index + 1
        else:
            # don't encode non alpha characters
            newcharacter = character
        encoded = encoded + newcharacter
    print encoded

# infinite loop over input
# we avoid infinitely looping on a file by looking for an empty input string
# otherwise allows user to type and encrypt/decrypt indefinitely until ended
while(1):
	INPUT_STR = sys.stdin.readline().rstrip("\n")
	if (INPUT_STR == ""):
		break
	encoded_key = keySetup(str(KEY), OPTION)
	encode(INPUT_STR, encoded_key)
