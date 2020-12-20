#!/bin/bash
# this is the install script
sudo cp proxmoxwol-listener.py /usr/bin/
sudo chmod 744 /usr/bin/proxmoxwol-listener.py
sudo chown root:root /usr/bin/proxmoxwol-listener.py
sudo cp proxmoxwol-vm.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/proxmoxwol-vm.service
sudo chown root:root /etc/systemd/system/proxmoxwol-vm.service
