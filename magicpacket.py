#!/bin/python
# simple script to send magic packets


import sys
import binascii
from socket import *

mac = ''

if len(sys.argv)<2:
    print("You need to specify a payload. Generally this is a MAC address")
    sys.exit(0)

if len(sys.argv[1]) > 17:
    mac = sys.argv[1][0:17]
else:
    mac = sys.argv[1]

mac = ''.join(mac.split(':'))
mac = mac.upper()
payload = 'FFFFFFFFFFFF'

for i in range(0,16):
    payload = payload + mac

payload = binascii.unhexlify(payload)

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.sendto(payload, ('255.255.255.255', 9))
