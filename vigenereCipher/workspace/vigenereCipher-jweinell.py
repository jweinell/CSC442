#!/usr/bin/python

import sys

def keySetup(key, encoding):
    key = "".join(key.lower().split())
    keyarray = []
    for letter in key:
        if encoding:
            keyarray.append(ord(letter) - 97)
        else:
            keyarray.append(26 - (ord(letter) - 97))
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
        else:
            newcharacter = character
        index = index + 1
        encoded = encoded + newcharacter
    print encoded

key = keySetup("my Key", False)
encode("tcvPm!12 r4",key)
