# Proxmox WOL server

This is a service written in python to wake VMs using WOL. It runs in systemd. It is known to work on proxmox.

### Why?

Proxmox virtual nics don't seem to respond to WOL packets. This service looks out for them and wakes your sleeping vms.

### How?

```
# git clone https://github.com/jd1123/proxmoxwol
# cd proxmoxwol
# ./install.sh
# sudo systemctl daemon-reload
# sudo systemctl start proxmox-vm.servive
```
