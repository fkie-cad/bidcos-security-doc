#!/usr/bin/env python3

import argparse, secrets, sys

from Crypto.Cipher import AES

def build_payload(msg_nbr, key_index, old_key, new_key):

    # Calculate counter & check which part of the key should be send
    if msg_nbr == 1:
        counter = key_index*2
        new_key = new_key[:16]
    else:
        counter = (key_index*2)+1
        new_key = new_key[16:]

    # Build payload
    payload = "{}{}{}{}{}".format("01", str(counter).zfill(2), new_key, secrets.token_hex(2).upper(), "7E296FA5")
    # Encrypt payload
    cipher = AES.new(bytes.fromhex(old_key), AES.MODE_ECB)
    payload = cipher.encrypt(bytes.fromhex(payload)).hex().upper()

    return payload

def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    # todo
    parser.add_argument('-n', '--messageNumber',
                        action='store',
                        type=int,
                        choices=[1, 2],
                        required=True)
    parser.add_argument('-i', '--keyIndex',
                        action='store',
                        type=int,
                        required=True)
    parser.add_argument('-o',
                        '--oldKey',
                        action='store',
                        type=str)
    parser.add_argument('-k',
                        '--newKey',
                        action='store',
                        type=str,
                        required=True)

    return parser.parse_args()

def main():
    # Default key
    old_key = '<<ADD DEFAULT KEY HERE>>'

    args = get_commandline_arguments()

    # Check if custom AES key is passed
    if args.oldKey is not None:
        old_key = args.oldKey.upper()

    payload = build_payload(args.messageNumber, args.keyIndex, old_key, args.newKey)

    # Convert hex to bit
    payload = format(int(payload, 16), "040b")

    # Pad missing zeros
    payload = str(payload).rjust(128, '0')

    sys.stdout.write(payload)

if __name__ == "__main__":
    main()
