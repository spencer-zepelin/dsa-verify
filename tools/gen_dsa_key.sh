#!/usr/bin/env sh

if [ ! "$#" -eq 3 ]; then 
    echo "Usage: gen_dsa_key.sh <size> <prv key file> <pub key file>"
    exit 1
fi

# NOTE: starting with DER caused errors on departmental machines, so I
# start with a PEM key and convert to a DER key

openssl dsaparam -outform PEM -genkey $1 > tmp.pem

openssl dsa -inform PEM -outform DER <tmp.pem >$2

rm tmp.pem

openssl dsa -inform DER -in $2 -text

openssl dsa -pubout -inform DER -in $2 -outform DER -out $3

