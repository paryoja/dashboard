import string
import random
import os
import sys

# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
if os.path.exists('./secret.txt'):
    print("secret file exists")
    sys.exit(0)

chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

with open('./secret.txt', 'w') as w:
    w.write(SECRET_KEY)
