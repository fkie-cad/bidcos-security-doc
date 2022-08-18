#!/usr/bin/env python3

import requests, datetime, sys
from dataclasses import dataclass
from Crypto.Cipher import AES

default_key = '<<ADD DEFAULT KEY HERE>>'


@dataclass
class Payload:
    subtype: str
    index: str
    key_part: str
    random: str
    magic_nbrs: str


def decrypt_md5(key):
    # Try to find hash in rainbow table
    params = {'hash': key,
              'hash_type': 'md5',
              'email': '<<ADD E-MAIL HERE>>',
              'code': '<<ADD CODE HERE>>'
              }
    r = requests.get('https://md5decrypt.net/en/Api/api.php', params=params)
    return r.content.decode("utf-8")


def extract_aes_key(msgs):
    cipher = AES.new(bytes.fromhex(default_key), AES.MODE_ECB)

    # Decrypt messages and cut parameters
    for i in range(2):
        msgs[i] = cipher.decrypt(bytes.fromhex(msgs[i][20:52])).hex().upper()

    # Assign fields
    payload1 = Payload(msgs[0][:2], msgs[0][2:4], msgs[0][4:20], msgs[0][20:24], msgs[0][24:32])
    payload2 = Payload(msgs[1][:2], msgs[1][2:4], msgs[1][4:20], msgs[1][20:24], msgs[1][24:32])

    key = payload1.key_part + payload2.key_part
    return key, payload1, payload2


def get_messages():
    # Read all msgs
    msgs = sys.stdin.readlines()

    target_msgs = []

    for msg in msgs:

        if "(" in msg:
            # Remove '(B->A):' ("Trigger Command")
            msg = msg.split(': ')[1]
        else:
            # Remove '->' ("External Program")
            msg = msg[2:]

        # Bit to Hex
        msg = '%08X' % int(msg, 2)
        # Cut preamble + sync
        msg = msg[16:]

        # Find KEY_EXCHANGE messages with type 0x04
        if msg[6:8] == '04':
            target_msgs.append(msg)

    return target_msgs

def log(key_msgs, key, payload1, payload2, decrypted_key):
    with open('../log.txt', 'a') as log_file:
        log_file.write("[{}] GET AES KEY\n"
                  "  Key:           {}\n"
                  "  Key decrypted: {}\n\n"
                  "  EncPayload_1:  {}\n"
                  "  EncPayload_2:  {}\n"
                  "                 ST IX KEY_PART         RAND MAGIC\n"
                  "  Payload_1:     {} {} {} {} {}\n"
                  "  Payload_2:     {} {} {} {} {}\n\n".format(datetime.datetime.now().strftime('%H:%M:%S %e-%m-%Y'),
                                                               key,
                                                               decrypted_key, key_msgs[0], key_msgs[1], payload1.subtype,
                                                               payload1.index, payload1.key_part, payload1.random,
                                                               payload1.magic_nbrs, payload2.subtype, payload2.index,
                                                               payload2.key_part, payload2.random, payload2.magic_nbrs))

def main():
    # Get necessary messages
    key_msgs = get_messages()

    key, payload1, payload2 = extract_aes_key(key_msgs.copy())

    decrypted_key = decrypt_md5(key)

    sys.stdout.write("AES-Key: " + key + " | See the log file for more information.")

    log(key_msgs, key, payload1, payload2, decrypted_key)

if __name__ == "__main__":
    main()
