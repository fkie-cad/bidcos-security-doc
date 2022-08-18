#!/usr/bin/env python3

import argparse, secrets
from Crypto.Cipher import AES


def decrypt_response(m_frame, c_frame, r_frame, key, a_frame=None):
    challenge = c_frame[22:34]
    # Pad zeros to challenge field to get to 32 chars
    challenge = challenge.ljust(32, '0')

    # XOR the default Key with the challenge field (without subtype) to get a temp key
    tmp_key = hex(int(key, 16) ^ int(challenge, 16))[2:].upper()
    tmp_key = tmp_key.rjust(32, '0')

    parameter = m_frame[22:54] # Changed
    payload = r_frame[20:52]
    iv = parameter.ljust(32, '0')

    cipher_pd = AES.new(bytes.fromhex(tmp_key), AES.MODE_CBC, bytes.fromhex(iv))
    pd = cipher_pd.decrypt(bytes.fromhex(payload)).hex().upper()

    cipher_pdd = AES.new(bytes.fromhex(tmp_key), AES.MODE_ECB)
    pdd = cipher_pdd.decrypt(bytes.fromhex(pd)).hex().upper()
    print("DECRYPT RESPONSE\n"
          "-------------------------------------------\n"
          "M-Frame:         {}\n"
          "C-Frame:         {}\n"
          "R-Frame:         {}\n\n"
          "Challenge:       {}\n"
          "Key:             {}\n"
          "Tmp key:         {}\n"
          "Payload:         {}\n"
          "IV:              {}\n"
          "Pd:              {}\n"
          "Pd^:             {}\n"
          "-------------------------------------------\n"
          "M-Frame:         {} {} {} {} {} {} {} {}\n"
          "DecrPayload:        {} {} {} {} {} {}\n"
          "Correct:         {}\n"
          "Auth:            {}\n"
          "Time token:      {}\n"
          "-------------------------------------------".format(m_frame, c_frame, r_frame, challenge, key, tmp_key,
                                                               payload, iv, pd, pdd, m_frame[0:2], m_frame[2:4],
                                                               m_frame[4:6], m_frame[6:8], m_frame[8:14],
                                                               m_frame[14:20], m_frame[20:22], m_frame[22:30],
                                                               pdd[12:14],
                                                               pdd[14:16], pdd[16:18], pdd[18:24], pdd[24:30],
                                                               pdd[30:32], m_frame[2:22] == pdd[12:32], pd[0:8],
                                                               pdd[0:12]))
    if a_frame is not None:
        print("A-Frame:         {} {}\n"
              "Auth:                                   {}\n"
              "Correct:         {}\n"
              "-------------------------------------------".format(a_frame[:22], a_frame[22:30], pd[0:8],
                                                                   a_frame[22:30] == pd[0:8]))


def generate_response(m_frame, c_frame, key, *args):
    r_frame, time_token = None, None
    for arg in args:
        if len(arg) > 12:
            r_frame = arg
        if len(arg) == 12:
            time_token = arg

    challenge = c_frame[22:34]
    # Pad zeros to challenge field to get to 32 chars
    challenge = challenge.ljust(32, '0')

    # XOR the default Key with the challenge field (without subtype) to get a temp key
    tmp_key = hex(int(key, 16) ^ int(challenge, 16))[2:].upper()
    tmp_key = tmp_key.rjust(32, '0')

    # Generate a random 12 char long hex value
    if time_token is None:
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
    parameter_m_frame = m_frame[22:54] # Changed
    iv = parameter_m_frame.ljust(32, '0')

    # Encrypt pd with the temp key and the zero IV
    cipher_pdd = AES.new(bytes.fromhex(tmp_key), AES.MODE_CBC, bytes.fromhex(iv))
    pdd = cipher_pdd.encrypt(bytes.fromhex(pd)).hex().upper()

    # Convert HEX to binary
    bit_pdd = format(int(pdd, 16), "040b")

    # Pad 0 to 128
    bit_pdd = str(bit_pdd).rjust(128, '0')

    print("GENERATE RESPONSE:\n"
          "-------------------------------------------\n"
          "M-Frame:         {}\n"
          "C-Frame:         {}\n\n"
          "Challenge:       {}\n"
          "Key:             {}\n"
          "Tmp key:         {}\n"
          "Time token:      {}\n"
          "Env M-Frame:     {}\n"
          "EncrPayload:     {}\n"
          "Pd:              {}\n"
          "IV:              {}\n"
          "-------------------------------------------\n"
          "AES-Payload:     {}\n"
          "Bin-AES-Payload: {}\n"
          "-------------------------------------------".format(m_frame, c_frame, challenge, key, tmp_key, time_token,
                                                               env_m_frame, payload, pd, iv, pdd, bit_pdd))
    if r_frame is not None:
        print("R-Frame:     {} {} {} {} {} {} {}\n"
              "GenPayload:                            {}\n"
              "Correct:     {}\n"
              "-------------------------------------------\n".format(r_frame[0:2], r_frame[2:4], r_frame[4:6],
                                                                     r_frame[6:8], r_frame[8:14], r_frame[14:20],
                                                                     r_frame[20:52], pdd, r_frame[20:52] == pdd))


def get_commandline_arguments():
    parser = argparse.ArgumentParser(description="Debugging tool for HomeMatic CR.")
    parser.add_argument('-d',
                        '--decrypt',
                        action='store',
                        type=str,
                        nargs='*',
                        help='[M-Frame] [C-Frame] [R-Frame] {A-Frame}')
    parser.add_argument('-g', '--generate',
                        action='store',
                        type=str,
                        nargs='*',
                        help='[M-Frame] [C-Frame] {R-Frame} {Time token}')
    # Random generated, with time token, compare to r-Frame
    parser.add_argument('-k', '--key',
                        action='store',
                        type=str,
                        help='{key}')

    return parser.parse_args()


def main():
    # Default key
    key = '<<ADD DEFAULT KEY HERE>>'

    args = get_commandline_arguments()


    # --key
    if args.key is not None:
        key = args.key


    # --decrypt
    if args.decrypt is not None:
        # Cut preamble + sync
        for i in range(len(args.decrypt)):
            args.decrypt[i] = args.decrypt[i].upper()
            if "E9CAE9CA" in args.decrypt[i]:
                args.decrypt[i] = args.decrypt[i][args.decrypt[i].index("E9CAE9CA") + 8:]

        if len(args.decrypt) == 3:
            decrypt_response(args.decrypt[0], args.decrypt[1], args.decrypt[2], key)
        elif len(args.decrypt) == 4:
            decrypt_response(args.decrypt[0], args.decrypt[1], args.decrypt[2], key, args.decrypt[3])


    # --generate
    if args.generate is not None:
        # Cut preamble + sync
        for i in range(len(args.generate)):
            args.generate[i] = args.generate[i].upper()
            if "E9CAE9CA" in args.generate[i]:
                args.generate[i] = args.generate[i][args.generate[i].index("E9CAE9CA") + 8:]

        if len(args.generate) == 2:
            generate_response(args.generate[0], args.generate[1], key)
        elif len(args.generate) == 3:
            generate_response(args.generate[0], args.generate[1], key, args.generate[2])
        elif len(args.generate) == 4:
            generate_response(args.generate[0], args.generate[1], key, args.generate[2], args.generate[3])



if __name__ == "__main__":
    main()
