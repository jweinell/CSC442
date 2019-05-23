# XOR Crypto Programming Assignment
# Group 1 - Macedonians
import sys, os

# DEBUG activator
DEBUG = 1

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

	# if the key and input don't match size, 
	# loop the key to match the size of the input
	if len(key) != len(input_text):
		if len(key) < len(input_text): 
			# if the key is shorter than the input, we need to expand the key
			# to match the length of the input by looping
			while (len(key) != len(input_text)):
				# if there is more space remaining to be filled than the key has length
				if len(key) < (len(input_text) - len(key)):
					key += key
				# if there isn't enough room to paste in the whole key, we paste in a part
				else:
					val = len(input_text) - len(key)
					key += key[0:val]
		else:
			# if we reach this, the input is shorter than our key
			# so shrink the key to match the input
			key = key[:len(input_text)]

	if (DEBUG):
		if (len(key) == len(input_text)):
			print "Key and input match length: {}".format(len(key))
		else:
			print "key and input don't match: {} and {}".format(len(key), len(input))

	# takes the XOR of each ASCII character and stores it into a list
	output_str = ""
	i = 0
	while i < len(input_text):
		output_str += chr(ord(input_text[i]) ^ ord(key[i]))
		i += 1

	sys.stdout.write(output_str)

## MAIN CODE ##
XOR()