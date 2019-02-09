#!/usr/bin/python2.7
#simple python client sample code from Tutorials Point: https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from time import sleep

# SOME META DATA:
netid = "tk1931\n" # needed as identifier for the challenge
numbers = {
    "ONE": "1",
    "TWO": "2",
    "THREE": "3",
    "FOUR": "4",
    "FIVE": "5",
    "SIX": "6",
    "SEVEN": "7",
    "EIGHT": "8",
    "NINE": "9",
    "ZERO": "0"
}

# SOCKET DEFINITIONS
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = "offsec-chalbroker.osiris.cyber.nyu.edu"   # Get local machine name (from challenge)
port = 1236                # port for the remote server
buffer = 1024
received = None

# DO STUFF
try: 
    s.connect((host, port))     #connect to the host
    received = s.recv(buffer)
    print(received)
    
    # send metadata
    if (s.send(netid) > 0) :
        print(netid)
    else :
        raise Exception() 
    
    while True:
        sleep(0.1)
        received = s.recv(buffer)
        if "= ?" in received : #its a math problem
            # start doing math
            # second to last is chosen in case of extra comments and to get around newline
            math = received.split('\n')[-2]
            parsedList = (math.split(' ')[0:3]) # assuming that all problems are two inputs and an operand
            for i in range(len(parsedList)) :
                o = parsedList[i] 
                if o.isdigit() : # the problem has numbers
                    continue
                elif o in [ "-", "*", "/", "+"] :
                    continue
                else : # a non-decimal input
                    translation = ""
                    if "0x" in o : # hex input
                        translation = str(int(o, 16))
                    elif "0b" in o: # binary input
                        translation = str(int(o, 2))
                    else : # word input
                        for z in o.split("-") :
                            translation += numbers[z]
                    parsedList[i] = translation
            
            parsedText = ''.join(parsedList)
            answer = str(eval(parsedText))
            print(parsedText + " = " + answer)
            s.send(answer + "\n")
        else :
            print(received)
except Exception as e:
    print("Something went wrong with statement:\n" + received)
    print(e)
    s.close()
finally:
    s.close()                     # Close the socket when done