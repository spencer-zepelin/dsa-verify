Applied Cryptography
MPCS 56530

DSA Signature Verification
Project 4

Spencer Zepelin

December 1, 2019

------------------


Building and Running the Program
---

The program can be run in any environment with a recent version of Python 3 and 
the pip utility. It makes use of the "cryptography" library for decoding and 
parsing the key and signature files. This can be installed with the following 
command:

	pip install cryptography

If the user is familiar with virtual environments or Anaconda, I strongly 
encourage this program to be tested in a clean virtual environment to ensure 
there are no naming collisions.

The only other dependencies are in the Python Standard Library.

The program performs only a single operation: Verification of a DSA signature.
The public keyfile, message file, and signature file are all passed to the 
program which will then indicate whether or not it was able to successfully
verify the signature.

Usage:
python dsaverify.py  <PUBLIC KEY FILEPATH> <INITIAL FILE FILEPATH> <SIGNATURE FILEPATH>


Program Design 
---

The program is relatively simple. It reads and parses the three files for their
relevant components. For the message file, it updates the SHA256 hash in Kilobyte 
chunks to conserve memory. 

Once the program has the necessary components from the files, it implements the DSA
Signature Verification algorithm and prints its result.

In service of the algorithm, two helper functions were built. One
implements the Extended Euclidean Algorithm to find a modular multiplicative
inverse, and the other implements the Square-then-Multiply Algorithm for 
modular exponentiation by large values.


Testing and Issues
---

OpenSSL provides the necessary tools to test the proper functioning of this program.
3072 bit keys can be generated and used to sign an arbitrary file. The results from 
this program can then be compared to those obtained using OpenSSL signature 
verification.

Following this pattern, the program passed all tests using 2048 and 3072 bit key pairs.
While DSA accepts smaller keys (1024 bit), the default message digest in OpenSSL does 
not use SHA256 and thus this program will not verify correctly.
