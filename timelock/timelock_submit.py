import hashlib
import datetime
import pytz
import dateutil
import sys

# TIMELOCK Code: Group 1, Macedonians

#### NOTE: THIS CODE REQUIRES PYTZ / DATEUTIL LIBRARY. MUST BE INSTALLED BEFORE RUNNING. ####
#### pip install pytz ####
#### pip install python-dateutil ####
#### NOTE: Set to work based on a CST/CDT local clock.

# datetimes should be stored as YYYY MM DD HH mm SS
# "epoch" time is given through stdin
INPUT_EPOCH = sys.stdin.readline().strip()

# turn the input into a valid datetime object
timezone = pytz.timezone('America/Chicago')
utc = pytz.UTC

# give it some default time zone, then convert all to UTC
epoch = INPUT_EPOCH.split()
epoch = datetime.datetime(int(epoch[0]),int(epoch[1]),int(epoch[2]),int(epoch[3]),int(epoch[4]),int(epoch[5]))
epoch = timezone.localize(epoch)
epoch = epoch.astimezone(utc)
epoch = epoch.replace(tzinfo=None)
# current time is just whatever time it is now
current = datetime.datetime.utcnow()

# calculate the time difference between the epoch and the current time
time_elapsed = (current - epoch).total_seconds()

# we want hashes to be valid for 60 seconds, which means we can mod 60
# and subtract those differences
time_elapsed = time_elapsed - (time_elapsed % 60)

time_elapsed_round = long(time_elapsed)

# now based on THIS time difference, we perform the double MD5 hashing.
hashed = hashlib.md5(hashlib.md5(str(time_elapsed_round)).hexdigest()).hexdigest()

# now we need to convert this into our specific key
output = ""
counter_af = 0
counter_09 = 0
# grab the first two characters
for item in hashed:
	if counter_af >= 2:
		break
	elif item.isalpha() == True:
		output += item
		counter_af += 1
# grab the first two numbers from reverse order
hashed_rev = hashed[::-1]
for item in hashed_rev:
	if counter_09 >= 2:
		break
	elif item.isdigit() == True:
		output += item
		counter_09 += 1
# add extra bit
output += hashed_rev[0]
print output
