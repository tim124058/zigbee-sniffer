#!/usr/bin/env python3
import subprocess
import os,sys,shutil
import pathlib
import re


def checkCmd():
    required_command = ["zbstumbler","zbdump","zbwireshark","wireshark","tshark"]
    for i in required_command:
        if not shutil.which(i):
            sys.exit("[ERROR] %s command not found.\n\tInstall command: ./install.sh" % (i))

def Menu():
    print("")
    print("####################")
    print("## zigbee sniffer ##")
    print("####################")
    print("1. scan zigbee channel")
    print("2. get key and decrypt")
    print("3. sniff zigbee traffic")
    print("4. exit")
    c = input("> ")
    print("")
    return c

def scan():
    print("[INFO] scanning zigbee device, press ctrl+c to stop scan...\n")
    os.system("sudo zbstumbler")
    print("\n")

def getkey():
    channel = input("select channel: ")
    name = input("output pcap filename: ")
    print("[INFO] please add new zigbee device")
    print("[INFO] press ctrl+c to stop...\n")
    try:
        os.system("sudo zbdump -c %s -w %s" % (channel, name))
        print("[INFO] zbdump has been stopped")

        # config path
        folders = subprocess.check_output("tshark -G folders".split()).decode()
        f = re.findall("Personal configuration:[ \t](.*?)\n",folders)
        if len(f):
            pathlib.Path(f[0]).mkdir(parents=True, exist_ok=True)
            f = f[0] + "/zigbee_pc_keys"

            # add zigbee default key to config path
            os.system("sudo cp ./zigbee_pc_keys %s" % (f))

            # find the transport key from the previously obtained pcap file and than add it to the config file
            key = subprocess.check_output(('tshark -r %s -Y zbee_aps.cmd.key -T fields -e zbee_aps.cmd.key' % (name)).split()).decode()
            key = key.replace(":","")
            if key:
                key = list(set(key.split("\n")) - {''})
                for i in key:
                    print("* found key : " + repr(i) + " *")
                    pre_key = '\'"%s","Normal",""\'' % (i)
                    os.system('echo %s | sudo tee -a %s 1>/dev/null' % (pre_key, f))
            else:
                print("key not found")
        else:
            print("[ERROR] tshark configuration folder not found!")
            return 0
    except:
        import traceback
        traceback.print_exc()
        print("[ERROR] known error")
    print("\n")

def sniffMenu():
    print("")
    print("# sniff zigbee traffic #")
    print("1. sniff with wireshark")
    print("2. sniff with zbdump")
    print("3. open pcap file with wireshark")
    print("4. exit")
    c = input("sniff > ")
    print("")
    return c

def s_wireshark():
    channel = input("select channel: ")
    os.system("sudo zbwireshark -c %s" % (channel))

def s_dump():
    channel = input("select channel: ")
    name = input("output pcap filename: ")
    print("[INFO] press ctrl+c to stop...\n")
    os.system("sudo zbdump -c %s -w %s" % (channel, name))

def wireshark():
    name = input("pcap filename: ")
    os.system("wireshark %s" % name)

def sniff():
    while True:
        try:
            c = sniffMenu()
            if c == "1":
                s_wireshark()
            elif c == "2":
                s_dump()
            elif c == "3":
                wireshark()
            elif c == "4":
                return 0
            else:
                print("command not found!")
        except KeyboardInterrupt:
            return 0

def main():
    checkCmd()
    while True:
        try:
            c = Menu()
            if c == "1":
                scan()
            elif c == "2":
                getkey()
            elif c == "3":
                sniff()
            elif c == "4" or c == "exit":
                sys.exit()
            else:
                print("command not found!")
        except KeyboardInterrupt:
            print('\nEnter 4 to exit')
        except Exception as e:
            print('[ERROR] known error')

if __name__ == '__main__':
    main()

