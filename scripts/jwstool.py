#!/usr/bin/env python3

import argparse
import json
import rfc8785
import sys

from jwcrypto import jwk, jws
from jwcrypto.common import base64url_encode, base64url_decode

def canonicalize(obj):
    return rfc8785.dumps(obj)

def pem2jwk(pem_key, algorithm=None):
    key = jwk.construct(pem_key, algorithm=algorithm)
    return key.to_dict()

def load_key(filename):
    try:
        with open(filename, "rb") as pem_file:
            return pem_file.read()
    except Exception as e:
        print(f"Failed to load key file '{filename}': {e}", file=sys.stderr)
        exit(2)

def load_file(filename):
    data = None
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON file '{filename}': {e}", file=sys.stderr)
        exit(2)
    return data

def write_file(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except Exception as e:
        print(f"Failed to write JSON file '{filename}': {e}", file=sys.stderr)
        exit(2)

def sign(key, filename, algorithm):
    data = load_file(filename)    
    if 'signature' in data[list(data.keys())[0]]:
        print(f"JSON file '{filename} is already signed.", file=sys.stderr)
        exit(2)

    c_data = canonicalize(data)
    headers = {"alg": algorithm}
    c_headers = canonicalize(headers)

    key = jwk.JWK.from_pem(key)
    signed = jws.JWS(c_data)
    try:
        signed.add_signature(
            key=key,
            header=None,
            protected=c_headers.decode('utf-8'),
        )
    except TypeError:
        print(f"Failed to create signature. Are you using a private key?",
              file=sys.stderr)
        sys.exit(2)
    jws_dict = json.loads(signed.serialize(compact=False))
    jws_object = {
        "signatures": [{
            "protected": jws_dict["protected"],
            "signature": jws_dict["signature"],
        }]
    }
    write_file(jws_object, f"{filename}.jws")
    print(f"Signature writen to {filename}.jws.")

def validate(key, filename, algorithm):
    data = load_file(filename)
    jws_object = load_file(f"{filename}.jws")
    c_data = canonicalize(data)
    jws_object["payload"] = base64url_encode(c_data)
    verifier = jws.JWS()
    verifier.deserialize(json.dumps(jws_object))
    key = jwk.JWK.from_pem(key)
    try:
        verifier.verify(key)
        print("Signature is valid.")
    except Exception as e:
        print(f"Signature verification failed: {e}")

def main():
    argparser = argparse.ArgumentParser(description='JSON canonicalizer and signer')
    action = argparser.add_mutually_exclusive_group(required=True)
    action.add_argument('-s', '--sign', action='store_true', help='sign')
    action.add_argument('-v', '--validate', action='store_true', help='validate')
    argparser.add_argument('-k', '--key', required=True, help='key file')
    argparser.add_argument('-a', '--algorithm', default='ES512', help='algorithm')
    argparser.add_argument("filename", help="File name")
    args = argparser.parse_args()

    if args.sign:
        sign(key=load_key(args.key), algorithm=args.algorithm, filename=args.filename)
    elif args.validate:
        validate(key=load_key(args.key), algorithm=args.algorithm, filename=args.filename)

if __name__ == '__main__':
    main()
