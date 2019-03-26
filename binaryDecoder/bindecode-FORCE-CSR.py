#!/usr/bin/python
# written by Christopher Rice

# edited version to force a 7-style and 8-style attempt
# which could be an issue if ASCII w/ backspaces isn't evenly divisible
# in length by 7 or 8

# this is kind of a brute-force attempt and not really pretty, but could prove useful
# since his tricky.txt example just happened to work

import sys

def decode_to_ascii(binstr):
    # make sure input was actually passed in
    if len(binstr) == 0:
        return "Invalid input or empty input passed\n"

    # init the array we'll store into and check what kind of ascii we are decoding
    output = []
    flag = 0
    force_both = False

    # if the binary is divisible by 7 and 8, no easy way to tell which is needed
    # so we'll just do both
    if (len(binstr)%7 == 0 and len(binstr)%8 == 0):
        flag = 7
        force_both = True
        output2 = []
        binstr2 = binstr # create a copy for using
    # if we can tell it's just 7
    if len(binstr)%7 == 0:
        flag = 7
    # or just 8
    elif len(binstr)%8 == 0:
        flag = 8
    # otherwise we can't tell which it is (a mix of 7 with 8-bit backspaces)
    else:
        flag = 7
        force_both = True
        output2 = []
        binstr2 = binstr # create a copy for using

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

    # runs only if needing to do both
    if force_both:
        flag = 8
        # perform the actual decoding
        while len(binstr2) > 0:
            current = int(binstr2[0:flag], 2) # take group and convert to base 10

            # if a backspace was sent (thanks Gourd), no matter 7 or 8
            # also futureproofed, won't accept a backspace at first
            if int(binstr2[0:8], 2) == 8:
                if len(output2) == 0:
                    continue
                else:
                    del output2[-1]
                    binstr2 = binstr2[8:]
            # standard case of decoding
            else:
                current = chr(current) # convert to ASCII
                output2.append(current) # add to output list
                binstr2 = binstr2[flag:] # remove that character from the string we are iterating over

    # convert the character array into a string for printing
    # if unrecognized as 7 or 8 precisely
    if force_both:
        output_str = "7-bit attempt: {}".format("".join(output))
        output2_str = "8-bit attempt: {}".format("".join(output2))
        out = "{}\n{}".format(output_str, output2_str)
        return out
    # normal case
    else:
        output_str = "".join(output)
        return output_str

# main body, take input and run conversion
# then print result
input_data = sys.stdin.readline().strip()
print decode_to_ascii(input_data)