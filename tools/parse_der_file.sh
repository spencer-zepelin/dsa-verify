#!/usr/bin/env sh

if [ ! "$#" -eq 1 ]; then 
    echo "Usage: parse_der_file.sh <der file>"
    exit 1
fi

openssl asn1parse -inform DER <$1
