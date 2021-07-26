import nmap
import os
import socket as sc
from sys import platform
import sys

if platform == "linux" or platform == "linux2":
    os.system("clear")
if platform == "win32":
    os.system("cls")

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def help():
    print("     ", colored(0, 255, 0, commands[0]), "makes you exit.")
    print("     ",colored(0, 255, 0, commands[3]), "clear the screen")
    print("     ",colored(0, 255, 0, commands[2]), "prompt the help menu")
    print("\n")
    print("     ",colored(0, 255, 0, commands[1]), "show the alive devices on your local network")
    print("     ",colored(0, 255, 0, commands[4]), "check vulnerabilities on your local network")



def scan():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan = nm.scan(hosts= myip , arguments='-sn')
    for i in scan['scan']:
        brand = list(scan['scan'][i]['vendor'].values())
        name = scan['scan'][i]['hostnames'][0]['name']
        if len(brand) == 1:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, brand[0]), "and called", colored(0, 255, 150, name), "is up")
        else:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, "Unknown"), "and called", colored(0, 255, 150, name), "is up")

def scan_vuln():
    nm = nmap.PortScanner()
    myip = local_ip+"/24"
    scan = nm.scan(hosts= myip , arguments='--script vuln')
    print(scan['scan'])
    for i in scan['scan']:
        brand = list(scan['scan'][i]['vendor'].values())
        name = scan['scan'][i]['hostnames'][0]['name']
        if len(brand) == 1:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, brand[0]), "and called", colored(0, 255, 150, name), "is up")
        else:
            print(colored(0, 255, 0, i), "made by", colored(0, 255, 150, "Unknown"), "and called", colored(0, 255, 150, name), "is up")

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
            if  cmd == "scan vuln":
                scan_vuln()
        else:
            print("\n")
            print(colored(255, 0, 0, "      '{}'".format(cmd)), colored(50, 50, 150, " is not a command, use help to see all the commands."))
        print("\n")

print("    ,%@@@@@@%(,.                   .,#                                              \n")
print("                           *@@@@@@@@@*@                                             \n")
print("                   @@@,                @*             &                             \n")
print("            @@                          @@@@@@@@@@@,      *                         \n")
print("      @@                             (@@@&         .@@@@@*@   %                     \n")
print(" /%                                (@@#                   @@@@@ ,                   \n")
print("                                  %@@                          @@@@                 \n")
print("                                  @@                            #@@@                \n")
print("                                   @@@                                              \n")
print("                                    @@@@.                                           \n")
print("                                       *@@@@@@@@@@@@@@@@#                           \n")
print("                                                        &@@@@@@@@@                  \n")
print("                                                              @@    %@@             \n")
print("                                                                 #@     .@          \n")
print("                                                                    @      @        \n")
print("                                                                      %      .      \n")
print("                                                                       @            \n")
print("                                                                        #           \n")

print("\n")

print(colored(255, 0, 0, "      Hello"), colored(0, 255, 0, "{}".format(sc.gethostname())), colored(255, 0, 0, "I am nobody."))
print("\n")

local_ip = sc.gethostbyname(sc.gethostname())

commands = ["exit", "scan", "help", "clear", "scan vuln"]

main()
