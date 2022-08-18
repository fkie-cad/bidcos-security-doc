/*  Universal Radio Hacker: investigate wireless protocols like a boss
    Copyright (C) 2022 Johannes Pohl and Andreas Noack

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <string.h>

#define SHORTEN_PREAMBLE_TO_32 0

typedef unsigned char byte;
typedef unsigned short uint16;

byte str2byte(char str[8])
{
    int ret = 0, i;
    for(i = 0; i < 8; i++)
        if (str[i]=='1') ret |= (1<<(7-i));
    return ret;
}

void print_binary(byte inpt)
{
    int i;
    for(i = 0; i < 8; i++)
        if (inpt & (1<<(7-i))) putchar('1');
        else putchar('0');
}

void print_preamble_nibbles(int count)
{
    int i;
    for (i = 0; i < count; i++)
        printf("1010");
}

int find_preamble_start_in_bit(char *string, int len)
{
    char homematic_sync[] = "11101001110010101110100111001010";    
    for(int i = 0, j = 0; i < len; i++)
    {
        if(string[i] == homematic_sync[j])
        {     
            j++;
            if(j == 32 && i>= 63) return i-63;            
        }
        else j = 0;
    }
    return -1; //not found
}

int main(int argc, char **argv)
{
    int i, j, max, offset, len, preamble_additional_length;
    byte dec[1024]={0}, enc[1024]={0};
    char string[65536]={0};
    offset = 8; // Preamble + Sync
    
    // Copy data (argv[2]) to string if length is ok, shorten to multiple of 8 bit
    if (strlen(argv[2]) > 8192*8 || strlen(argv[2]) < 4) return -1;
    len = strlen(argv[2]);    
    
    i = find_preamble_start_in_bit(argv[2], len);
    if(i < 0) return 0;    // preamble+sync not found or wrong length
    preamble_additional_length = i;
    
    len = (len-i)-(len-i)%8;
    memcpy(string, argv[2]+i, len);
               
    if (argc>2)
    {
        if (argv[1][0]=='d')
        {     
            // Pack to bytes
            for (i = 0; i < strlen(string)-3; i+=8)
                enc[i/8] = str2byte(&string[i]);                
            max = i/8;
            memcpy(&dec, &enc, 1024);

            
            /*
             * byte[] Dec = new byte[Enc.Length];
             * Dec[0] = Enc[0]; //Packet length
             * Dec[1] = (byte)((~Enc[1]) ^ 0x89);
             * int j;
             * for (j = 2; j < Dec[0]; j++)
             *   Dec[j] = (byte)((Enc[j-1] + 0xdc) ^ Enc[j]);
             * Dec[j] = (byte)(Enc[j] ^ Dec[2]);
             */
            
            // Decrypt
            dec[offset+0] = enc[offset+0];            
            dec[offset+1] = (~enc[offset+1])^0x89;            
            for(i = offset + 2; i < max - 3; i++)
                dec[i] = (enc[i-1]+0xdc) ^ enc[i];
            dec[i] = enc[i] ^ dec[offset+2];
            

            dec[max-1] = 0;
            dec[max-2] = 0;

            
            // Prepend preamble longer than 32 bits
            if(0 == SHORTEN_PREAMBLE_TO_32 && preamble_additional_length > 0) 
                print_preamble_nibbles(preamble_additional_length/4);
                
            for(i = 0; i < max; i++)
                print_binary(dec[i]);
        }
        else
        {
            // Pack to bytes
            for (i = 0; i < strlen(string)-3; i+=8)
                dec[i/8] = str2byte(&string[i]);
            max = i/8;
            memcpy(&enc, &dec, 1024);
            
            /*
             * byte[] Dec = new byte[Enc.Length];
             * Dec[0] = Enc[0]; //Packet length
             * Dec[1] = (byte)((~Enc[1]) ^ 0x89);
             * int j;
             * for (j = 2; j < Dec[0]; j++)
             *   Dec[j] = (byte)((Enc[j-1] + 0xdc) ^ Enc[j]);
             * Dec[j] = (byte)(Enc[j] ^ Dec[2]);
             */
            
            // Encrypt
            enc[offset+0] = dec[offset+0];            
            enc[offset+1] = ~(dec[offset+1])^0x89;            
            for(i = offset + 2; i < max - 3; i++)
                enc[i] = (enc[i-1]+0xdc) ^ dec[i];
            enc[i] = dec[i] ^ dec[offset+2];
            

            enc[max-1] = 0;
            enc[max-2] = 0;         
            
            // Convert to string
            memset(string, 0, 65536);
            for(i = 0; i < max; i++)
            {
                for(j = 0; j < 8; j++)
                    if(enc[i] & (1<<(7-j))) string[i*8+j]='1';
                    else string[i*8+j]='0';
            }

            // Prepend preamble longer than 32 bits
            if(0 == SHORTEN_PREAMBLE_TO_32 && preamble_additional_length > 0) // Add preamble longer than 32 bits
                print_preamble_nibbles(preamble_additional_length/4);
            
            // Print bits and duplicate last bit
            printf("%s%c\n", string, string[strlen(string)-1]);
        }
    }
    else printf("Usage: %s <d/e> <bit sequence>\n\td - decode\n\te - encode\n\tbit sequence as string of 0 and 1.\n", argv[0]);
    
    return 0;
} 
