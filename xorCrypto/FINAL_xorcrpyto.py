# XOR Crypto Programming Assignment
# Group 1 - Macedonians
import sys, os

# DEBUG activator
DEBUG = 0

def XOR():
	# collect the text to be encoded/decoded and what key we will be using
	# the input to be coded is given through stdin
	input_text = sys.stdin.read().rstrip('\n')

	# the key is from a file
	try:
		# opens the current directory appended with key and takes the data
		with open(os.path.join(os.path.dirname(__file__), "key")) as keyfile:
			key = keyfile.read().rstrip('\n')
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

	# takes the XOR of each ASCII character and stores it into a list
	output_str = ""
	i = 0
	while i < len(input_text):
		output_str += chr(ord(input_text[i]) ^ ord(key[i]))
		i += 1

	sys.stdout.write(output_str)

## MAIN CODE ##
XOR()