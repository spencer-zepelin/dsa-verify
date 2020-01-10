#!/usr/bin/env sh

if [ ! "$#" -eq 3 ]; then 
    echo "Usage: dsa_verify.sh <pub key file> <data file> <signature file>"
    exit 1
fi

openssl dgst -sha256 -keyform DER -verify $1 -signature $3 $2
