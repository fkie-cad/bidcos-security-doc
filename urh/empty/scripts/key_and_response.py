#!/usr/bin/env python3

import sys, argparse
import key_extractor
import response_generator

default_key = '<<ADD DEFAULT KEY HERE>>'

def get_messages(type):
    key_msgs = []
    m_frame, c_frame = "", ""

    msgs = sys.stdin.readlines()

    for i in range(len(msgs)):

        msg = msgs[i]

        # Remove '->' ("External Program")
        msg = msg[2:]

        # Bit to Hex
        msg = '%08X' % int(msg, 2)
        # Cut preamble + sync
        msg = msg[msg.index("E9CAE9CA")+8:]

        # Find KEY_EXCHANGE messages with type 0x04
        if msg[6:8] == '04':
            key_msgs.append(msg)

        # Find target messages
        if msg[6:8] == type:
            m_frame = msg
            c_frame = ('%08X' % int(msgs[i+1][2:], 2))[16:]
    return key_msgs, m_frame, c_frame

def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type',
                        action='store',
                        type=str,
                        required=True)

    return parser.parse_args()

def main():
    args = get_commandline_arguments()

    # Set target message type
    type = args.type

    # get necessary messages
    key_msgs, m_frame, c_frame = get_messages(type)

    # Get AES-Key
    key, payload1, payload2 = key_extractor.extract_aes_key(key_msgs.copy())
    decrypted_key = key_extractor.decrypt_md5(key)
    # Log
    key_extractor.log(key_msgs, key, payload1, payload2, decrypted_key)

    # Generate response
    aes_payload, aes_payload_hex, time_token = response_generator.generate_response(m_frame, c_frame, key)
    sys.stdout.write(aes_payload)
    # Log
    response_generator.log(key, m_frame, c_frame, aes_payload, aes_payload_hex, time_token)


if __name__ == "__main__":
    main()
