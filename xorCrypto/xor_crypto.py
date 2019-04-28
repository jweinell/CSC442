# XOR Crypto Programming Assignment
# Group 1 - Macedonians
import sys, os

# DEBUG activator
DEBUG = 0

def XOR():
	# collect the text to be encoded/decoded and what key we will be using
	# the input to be coded is given through stdin
	input_text = sys.stdin.readline().strip()

	# the key is from a file
	try:
		# opens the current directory appended with key and takes the data
		with open(os.path.join(os.path.dirname(__file__), "key")) as keyfile:
			key = keyfile.readline().strip()
	except IOError:
		print "No file found named key in current directory of script."
		exit()

	if (DEBUG):
		print "key: {}".format(key)
		print "input text: {}".format(input_text)

	# make sure they are the same size
	if (len(input_text) != len(key)):
		print "Error: key and input text lengths do not match (fatal)"
		exit(1)

	if (DEBUG):
		print "key and input text were the same size, valid"

	# now that we know the key and token are the same size, we can perform operations on them
	# but to be able to XOR them, they must be in their binary form first
	key_bin = ""
	input_bin = ""
	# turn the key/input into a binary string that we can perform actions on
	# REMINDER: THIS IS IN SEVEN-BIT ASCII
	for item in range(0, len(key) - 1):
		key_bin += str(bin(ord(key[item]))[2:])
	for item in range(0, len(input_text) - 1):
		input_bin += str(bin(ord(input_text[item]))[2:])

	if (DEBUG):
		print "key converted to binary: {}".format(key_bin)
		print "input converted to binary: {}".format(input_bin)

	# now we can generate our encoded output based on the key
	output_str = str(bin(int(key_bin, 2) ^ int(input_bin, 2))[2:])
	output_str = output_str[2:].zfill(len(key_bin))

	if (DEBUG):
		print "output str pre-ascii-reconversion: {}".format(output_str)

	# convert this back to ASCII
	ascii_output = decode_ascii(output_str, 7)
	sys.stdout.write(ascii_output)
		

# ASCII Decoder, from previous coding assignment
def decode_ascii(binstr, bits):
    modification = bits - len(binstr)%bits
    index = 0
    mod_list = []
    while index < modification:
        binstr = binstr + '0'
        index = index + 1
    chrarray = []
    while len(binstr) > 0:
        chrnum = int(binstr[:bits],2)
        if chrnum != 8:
            chrarray.append(chr(chrnum))
        else:
            if len(chrarray) > 0:
                chrarray = chrarray[:-1]
        binstr = binstr[bits:]
    decoded = "".join(chrarray)
    return decoded



## MAIN CODE ##
XOR()