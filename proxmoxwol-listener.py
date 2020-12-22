#!/bin/python3
# This is the listener

import socketserver
import binascii
import os
import logging
try:
    from systemd.journal import JournalHandler
    systemd_present = True
except ImportError:
    print('python-systemd does not appear to be present. Please install this for journald logging')
    systemd_present = False


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
        logger.info('{} wrote:'.format(self.client_address[0]))
        packet = self.parse_packet(data)
        self.getfilenames()
        if self.iswol(data):
            logger.info('WOL Packet found for mac {}...'.format(packet[1].upper()))
            if packet[1].upper() in self.d.keys():
                logger.info("...and waking up vm {}".format(d[packet[1].upper()]))
                self.wakemachine(self.d[packet[1].upper()])
            else:
                logger.info('...but it\'s not for this machine')

    def iswol(self, dat):
        if len(dat) != 102:
            return False
        if self.parse_packet(dat)[0].upper() != b'FFFFFFFFFFFF':
            return False
        newdat = binascii.hexlify(dat)[12:]
        n = 12
        packs = [newdat[i:i+n] for i in range(0, len(newdat), n)]
        if len(packs) != 16:
            return False
        return True

    def parse_packet(self, dat):
        return [binascii.hexlify(dat)[:12], binascii.hexlify(dat)[12:24]]

    def convertmac(self, mac):
        return ''.join(mac.split(':'))
    
    def wakemachine(self, qemu_id):
        os.system(self.resume_command + qemu_id)

    def parsefiles(self, filename):
        try:
            with open(self.configdir + filename, 'r') as f:
                for line in f:
                    if line[:4] == 'net0':
                        mac = line.split('=')[1].split(',')[0]
                        self.d[self.convertmac(mac.upper())] = filename.split('.')[0]
        except FileNotFoundError:
            logger.warning('Proxmox configuration files not found at {}'.format(self.configdir))

    def getfilenames(self):
        try:
            files = os.listdir(self.configdir)
            for f in files:
                self.parsefiles(f)
        except FileNotFoundError:
            logger.warning('Proxmox configuration files not found at {}'.format(self.configdir))


def run_server():
    HOST, PORT = '', 9
    server = socketserver.UDPServer((HOST, PORT), UDPListener)
    server.serve_forever()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    
    if systemd_present:
        journald_handler = JournalHandler()
        journald_handler.setFormatter(logging.Formatter(
            '[%(levelname)s] %(message)s'))
        logger.addHandler(journald_handler)
    
    logger.setLevel(logging.DEBUG)
    run_server()
