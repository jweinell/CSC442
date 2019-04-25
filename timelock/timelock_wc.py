import hashlib
import datetime
import pytz

#### NOTE: THIS CODE REQUIRES PYTZ LIBRARY. MUST BE INSTALLED BEFORE RUNNING. ####
#### pip install pytz ####

# datetimes should be stored as YYYY MM DD HH mm SS
# temporary testing values
# will later be taken in from stdin and etc.
INPUT_EPOCH = "1999 12 31 23 59 59"
CURRENT_TIME = "2017 04 23 18 02 30"

# turn the input into a valid datetime object
epoch = INPUT_EPOCH.split()
epoch = datetime.datetime(int(epoch[0]),int(epoch[1]),int(epoch[2]),int(epoch[3]),int(epoch[4]),int(epoch[5]))
print epoch
current = CURRENT_TIME.split()
current = datetime.datetime(int(current[0]),int(current[1]),int(current[2]),int(current[3]),int(current[4]),int(current[5]))
print current

# calculate the time difference between the epoch and the current time
time_elapsed = (current - epoch).total_seconds()
print time_elapsed

# we want hashes to be valid for 60 seconds, which means we can mod 60
# and subtract those differences
time_elapsed = time_elapsed - (time_elapsed % 60)
print time_elapsed

# now based on THIS time difference, we perform the double MD5 hashing.
hashed = hashlib.md5(hashlib.md5(str(time_elapsed)).hexdigest()).hexdigest()
print hashed
