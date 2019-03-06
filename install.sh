#!/bin/bash
# wireshark
sudo apt-get install -y wireshark tshark

# killerbee
sudo apt-get install -y git python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev
if [ ! -d "~/scapy" ]; then
    git clone https://github.com/secdev/scapy ~/scapy
    cd ~/scapy
    sudo python setup.py install
fi

if [ ! -d "~/killerbee" ]; then
    git clone https://github.com/riverloopsec/killerbee.git ~/killerbee
fi
cd ~/killerbee
git checkout release/2.7.1
sudo -H pip install rangeparser
sudo python setup.py install
