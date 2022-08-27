## FILE OF CODE TO SETUP DISSEMINATOR ##
import smtplib, ssl, re, os, subprocess, sys, shutil
import json, csv, datetime, time

## Display initiation ##
print("Initialising setup...")
time.sleep(2)

## Install all required modules ##
print("Installing required modules...")
time.sleep(1)
try:
    os.system("pip install -r requirements.txt")
except Exception as e:
    print("AN ERROR OCCURRED IN INSTALLING MODULES FROM THE REQUIREMENTS.TXT FILE. ERROR: {}".format(e))
    print("Setup will exit...")
    sys.exit(1)

