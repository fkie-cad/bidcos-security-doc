#!/usr/bin/env python3

import secrets, sys, argparse, datetime

from Crypto.Cipher import AES

def generate_response(m_frame, c_frame, key):

    challenge = c_frame[22:34]
    # Pad zeros to challenge field to get to 32 chars
    challenge = challenge.ljust(32, '0')

    # XOR the default Key with the challenge field (without subtype) to get a temp key
    tmp_key = hex(int(key, 16) ^ int(challenge, 16))[2:].upper()
    tmp_key = tmp_key.rjust(32, '0')

    # Generate a random 12 char long hex value
    time_token = secrets.token_hex(6).upper()
    env_m_frame = m_frame[2:22]
    # Generate the payload by appending the all parameters of the m_frame (except length) to the  random time token
    payload = time_token + env_m_frame

    # 32 zeros
    iv = "00000000000000000000000000000000"

    # Encrypt the aes payload with the temp key and the zero IV
    cipher_pd = AES.new(bytes.fromhex(tmp_key), AES.MODE_CBC, bytes.fromhex(iv))
    pd = cipher_pd.encrypt(bytes.fromhex(payload)).hex().upper()

    # New IV
    parameter_m_frame = m_frame[22:54]
    iv = parameter_m_frame.ljust(32, '0')

    # Encrypt pd with the temp key and the zero IV
    cipher_pdd = AES.new(bytes.fromhex(tmp_key), AES.MODE_CBC, bytes.fromhex(iv))
    pdd = cipher_pdd.encrypt(bytes.fromhex(pd)).hex().upper()

    # Convert HEX to binary
    bit_pdd = format(int(pdd, 16), "040b")

    # Pad 0 to 128
    aes_payload = str(bit_pdd).rjust(128, '0')

    return aes_payload, pdd, time_token

def get_messages(type):
    m_frame, c_frame = "", ""

    msgs = sys.stdin.readlines()

    for i in range(len(msgs)):

        msg = msgs[i]
        if "(" in msg:
            # Remove '(B->A):' ("Trigger Command")
            msg = msg.split(': ')[1]
        else:
            # Remove '->' ("External Program")
            msg = msg[2:]

        # Bit to Hex
        msg = '%08X' % int(msg, 2)
        # Cut preamble + sync
        msg = msg[msg.index("E9CAE9CA")+8:]

        # Find last target messages
        if msg[6:8] == type:
            m_frame = msg
            c_frame = ('%08X' % int(msgs[i+1][2:], 2))[16:]
    return m_frame, c_frame

def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type',
                        action='store',
                        type=str,
                        required=True)
    parser.add_argument('-k',
                        '--key',
                        action='store',
                        type=str)

    return parser.parse_args()

def log(key, m_frame, c_frame, aes_payload, aes_payload_hex, time_token):
    with open('../log.txt', 'a') as log_file:
        log_file.write("[{}] GENERATE RESPONSE\n"
                  "  Bin-AES-Payload: {}\n"
                  "  AES-Payload:     {}\n\n"
                  "  Key:             {}\n"
                  "  Time token:      {}\n\n"
                  "  MSG_1:           {}\n"
                  "  MSG_2:           {}\n".format(datetime.datetime.now().strftime('%H:%M:%S %e-%m-%Y'), aes_payload,
                                                   aes_payload_hex, key, time_token, m_frame, c_frame))

def main():
    # Default key
    key = '<<ADD DEFAULT KEY HERE>>'

    args = get_commandline_arguments()

    # Set target message type
    type = args.type

    # Check if custom AES key is passed
    if args.key is not None:
        key = args.key.upper()

    # Get necessary messages
    m_frame, c_frame = get_messages(type)

    aes_payload, aes_payload_hex, time_token = generate_response(m_frame, c_frame, key)

    sys.stdout.write(aes_payload)

    log(key, m_frame, c_frame, aes_payload, aes_payload_hex, time_token)

if __name__ == "__main__":
    main()
