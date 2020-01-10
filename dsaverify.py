import sys
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

"""
Usage examples
$ ./verify pubdsa.key file.bin file.bin.sig
Verified OK
$ ./verify pubdsa.key file.bin bad.sig
Verification Failure
"""

# Implementation of square-then-multiply algorithm
# Used for very large exponents w/ modulus
def exponent_mod(base, exponent, mod):
	r = base
	exponent_string = bin(exponent)[3:]
	for val in exponent_string:
		r = (r * r) % mod
		if int(val) == 1:
			r = (r * base) % mod
	return r

# Implementation of extended Euclidean algorithm
# Used for finding multiplicative inverse w/ modulus
def inverse_mod(a, mod):
	mod_init = mod
	y = 0
	x = 1
	while a > 1:
		q = a // mod
		temp = mod
		mod = a % mod
		a = temp
		
		temp = y
		y = x - (q * y)
		x = temp
	if (x < 0):
		x = x + mod_init
	return x

if __name__ == '__main__':

	# Check for correct number of arguments
	if len(sys.argv) != 4:
		sys.exit('\n---ERROR---\nInvalid number of arguments. Please use the following format:\n\n  python dsaverify.py <PUBLIC KEY FILEPATH> <INITIAL FILE FILEPATH> <SIGNATURE FILEPATH>\n\n')

	# Parse command line arguments
	keyfile = sys.argv[1]
	messagefile = sys.argv[2]
	sigfile = sys.argv[3]

	# Read in binary data from keyfile
	with open(keyfile, "rb") as f:
		raw = f.read()
	# Parse keyfile data
	key = load_der_public_key(raw, backend=default_backend())
	key_parts = key.public_numbers()
	# Break out components of DSA Public Key
	beta = key_parts.y
	p = key_parts.parameter_numbers.p
	q = key_parts.parameter_numbers.q
	g = key_parts.parameter_numbers.g

	# Instantiate sha256 hash object
	M = hashlib.sha256()
	# Read in 1024 byte chunks from signed file
	with open(messagefile, "rb") as f:
		chunk = f.read(1024)
		# Update hash object state
		while chunk:
			M.update(chunk)
			chunk = f.read(1024)
	# Recover hex version of hash
	message_hash = int(M.hexdigest(), 16)

	# Read in signature file binary
	with open(sigfile, "rb") as f:
		# Parse out signature parts
		r, s = decode_dss_signature(f.read())

	# First test value
	l_test = r % q

	# Find multiplicative invers of s mod q
	w = inverse_mod(s, q)

	# Assertion to validate correctness of helper function
	assert (w * s) % q == 1, "inverse mod failure"

	# First exponent in verification value
	x = (w * message_hash) % q
	# Second exponent in verification value
	y = (w * r) % q
	# g^x mod p
	r0 = exponent_mod(g, x, p)
	# beta ^ y mod p
	r1 = exponent_mod(beta, y, p)
	# Full verification value
	r_test = ((r0 * r1) % p) % q

	# If values match, signature verified
	if l_test == r_test:
		print("Verified OK")
	# Otherwise, failure
	else:
		print("Verification Failure")









