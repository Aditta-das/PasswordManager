import os, random, string
from pathlib import Path

def password():
	length = 13
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))

	return ''.join(random.choice(chars) for i in range(length))

# password()