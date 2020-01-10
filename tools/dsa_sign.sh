#!/usr/bin/env sh

if [ ! "$#" -eq 2 ]; then 
    echo "Usage: dsa_sign.sh <prv key file> <data file>"
    exit 1
fi

openssl dgst -sha256 -keyform DER -out $2.sig -sign $1 $2
