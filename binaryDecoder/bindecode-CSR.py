#!/usr/bin/python
# written by Christopher Rice

import sys

def decode_to_ascii(binstr):
    # make sure input was actually passed in
    if len(binstr) == 0:
        return "Invalid input or empty input passed\n"

    # init the array we'll store into and check what kind of ascii we are decoding
    output = []
    flag = 0
    if len(binstr)%7 == 0:
        flag = 7
    elif len(binstr)%8 == 0:
        flag = 8
    else:
        return "input not recognized as standard 7 or 8 bit ASCII, check file\n"

    # perform the actual decoding
    while len(binstr) > 0:
        current = int(binstr[0:flag], 2) # take group and convert to base 10

        # if a backspace was sent (thanks Gourd), no matter 7 or 8
        # also futureproofed, won't accept a backspace at first
        if int(binstr[0:8], 2) == 8:
            if len(output) == 0:
                continue
            else:
                del output[-1]
                binstr = binstr[8:]
        # standard case of decoding
        else:
            current = chr(current) # convert to ASCII
            output.append(current) # add to output list
            binstr = binstr[flag:] # remove that character from the string we are iterating over

    # convert the character array into a string for printing
    output_str = "".join(output)
    return output_str

# main body, take input and run conversion
# then print result
input_data = sys.stdin.readline().strip()
print decode_to_ascii(input_data)