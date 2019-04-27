# XOR Crypto Programming Assignment
# Group 1 - Macedonians
import sys, os

# collect the text to be encoded/decoded and what key we will be using
# the input to be coded is given through stdin
input_text = sys.stdin.readline().strip()

# the key is from a file
try:
	# opens the current directory appended with key and takes the data
	with open(os.path.join(os.path.dirname(__file__), "key")) as keyfile:
		key = keyfile.readline().strip()
except IOError:
	print "No file found named key in current directory of script.\n"
	exit()

print input_text
print key