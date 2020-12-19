#!/bin/python
# This is the listener

import socketserver
import binascii
import os
import daemon

class UDPListener(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.d = dict()
        self.configdir = '/etc/pve/qemu-server/'
        self.resume_command = 'qm resume '
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print('{} wrote:'.format(self.client_address[0]))
        packet = self.parse_packet(data)
        self.getfilenames()
        print(self.d)
        if packet[0].upper() == b'FFFFFFFFFFFF':
            if packet[1].upper() in self.d.keys():
                print("need to wake up", packet[1].upper())
                self.wakemachine(self.d[packet[1].upper()])


    def parse_packet(self, dat):
        return [binascii.hexlify(dat)[:12], binascii.hexlify(dat)[12:24]]

    def convertmac(self, mac):
        return ''.join(mac.split(':'))
    
    def wakemachine(self, qemu_id):
        os.system(self.resume_command + qemu_id)

    def parsefiles(self, filename):
        with open(self.configdir + filename, 'r') as f:
            for line in f:
                if line[:4] == 'net0':
                    mac = line.split('=')[1].split(',')[0]
                    self.d[self.convertmac(mac.upper())] = filename.split('.')[0]

    def getfilenames(self):
        files = os.listdir(self.configdir)
        for f in files:
            self.parsefiles(f)


if __name__ == '__main__':
    HOST, PORT = '', 9
    server = socketserver.UDPServer((HOST, PORT), UDPListener)
    server.serve_forever()
