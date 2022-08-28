## FILE OF CODE TO SETUP DISSEMINATOR ##
import os, sys, time

## Display initiation ##
print("Initialising setup...")
time.sleep(2)

## Install all required modules ##
print("Installing required modules...")
time.sleep(1)
print()
try:
    os.system("pip install -r requirements.txt")
except Exception as e:
    print("AN ERROR OCCURRED IN INSTALLING MODULES FROM THE REQUIREMENTS.TXT FILE. ERROR: {}".format(e))
    print("Setup will exit...")
    sys.exit(1)

import smtplib, ssl, re, subprocess, shutil
import json, csv, datetime
from dotenv import load_dotenv
load_dotenv()

##### FUNCTIONS #######
def getIndivEmailEntry(recNum=None, smart=False, emailDomain=False):
    if recNum != None:
        print()
        print("----")
        print("RECIPIENT {}".format(recNum + 1))
        print("----")
    print()
    while True:
        if not smart:
            email = input("Enter recipient's email: ")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email. Please try again.")
                continue
            else:
                break
        else:
            name = input("Enter recipient's name (to be prepended to email domain): ")
            email = '_'.join(name.lower().split(' ')) + emailDomain
            break
    while True:
        file = input("Enter recipient's target file: ")
        if not os.path.isfile(os.path.join(os.getcwd(), 'targetFiles', file)):
            print("File not found. Please try again.")
            continue
        else:
            break
    print()
    return email, file

def getEmailEntriesFromUser():
    emailEntries = {}
    print()
    recipientsNum = input("How many recipients would you like to add: ")
    while True:
        if not recipientsNum.isdigit():
            print("Please enter an integer. Try again.")
            recipientsNum = print("How many recipients would you like to add: ")
            continue
        else:
            recipientsNum = int(recipientsNum)
            break
    for recipientNum in range(recipientsNum):
        while True:
            email, file = getIndivEmailEntry(recNum=recipientNum)
            print("Data for recipient {}: Email: '{}', File: '{}'".format(recipientNum + 1, email, file))
            confirmation = input("Is this correct? (y/n): ")
            if confirmation.lower() == "y":
                emailEntries[email] = file
                print("Recipient {} added.".format(recipientNum + 1))
                break
            else:
                print("Repeating procedure for recipient {}....".format(recipientNum + 1))
                continue
    return emailEntries

def getEmailEntriesSmartVersion():
    emailEntries = {}
    print()
    emailDomain = input("Enter the common email domain of all recipient emails: ")
    while True:
        if not emailDomain.startswith("@"):
            print("All email domains must start with an '@' sign. Please try again.")
            emailDomain = input("Enter the common email domain of all recipient emails: ")
            continue
        else:
            break

    print()
    recipientsNum = input("How many recipients would you like to add: ")
    while True:
        if not recipientsNum.isdigit():
            print("Please enter an integer. Try again.")
            recipientsNum = print("How many recipients would you like to add: ")
            continue
        else:
            recipientsNum = int(recipientsNum)
            break

    for recipientNum in range(recipientsNum):
        while True:
            email, file = getIndivEmailEntry(recipientNum, smart=True, emailDomain=emailDomain)
            print("Data for recipient {}: Email: '{}', File: '{}'".format(recipientNum + 1, email, file))
            confirmation = input("Is this correct? (y/n): ")
            if confirmation.lower() == "y":
                emailEntries[email] = file
                print("Recipient {} added.".format(recipientNum + 1))
                break
            else:
                print("Repeating procedure for recipient {}....".format(recipientNum + 1))
                continue
    return emailEntries



def convertDictToCSVString(emailsDict):
    csvString = ""
    for email in emailsDict:
        csvString += "{},{}\n".format(email, emailsDict[email])
    return csvString

## Display Menu
print("""
Welcome to Setup! It is recommended that you refer to the README.md file (or look at the GitHub repository) 
for documentation on how to operate Setup and the actual Disseminator program.

Here is the menu of options you can choose from:

    1) Setup Disseminator (For newly-installed copies; generates csv and .env files)
    2) Add a new recipient email entry
    3) Delete a recipient email entry
    4) Edit a recipient email entry (edit recipient's email or target file)

""")
menuOption = input("Enter the choice number: ")
while True:
    if not menuOption.isdigit():
        print("Menu option number must be an integer. Please try again.")
        menuOption = input("Enter the choice number: ")
        continue
    else:
        menuOption = int(menuOption)
        break

## Setup Disseminator ##
if menuOption == 0:
    print("Setup will exit...")
    sys.exit(1)
elif menuOption == 1:
    print()
    print("Please wait while setup scans the environment for already present data files...")
    print()
    time.sleep(1)

    ### Check if .env file already exists ###
    if not os.path.isfile(os.path.join(os.getcwd(), '.env')):
        print(".env file not found. Creating now...")
        time.sleep(1)
        with open(os.path.join(os.getcwd(), '.env'), 'w') as f:
            newSenderEmail = input("Enter the sender's email: ")
            newSenderEmailAppPassword = input("Enter the senders' emails' Google Account's App Password: ")
            f.write("SenderEmailAppPassword={}\nSenderEmail={}".format(newSenderEmailAppPassword, newSenderEmail))
            print("Created .env file.")
    else:
        print("Found .env file. Reading data...")
        time.sleep(1)
        if 'SenderEmailAppPassword' not in os.environ:
            newSenderEmailAppPassword = input("SenderEmailAppPassword field not found in .env file. Please set now: ")
            os.system("echo '\nSenderEmailAppPassword={}' >> .env".format(newSenderEmailAppPassword))
        if 'SenderEmail' not in os.environ:
            newSenderEmail = input("SenderEmail field not found in .env file. Please set now: ")
            os.system("echo '\nSenderEmail={}' >> .env".format(newSenderEmail))
        print(".env file setup successfully.")
        
    print()
    
    ### Check if targetFiles folder already exists ###
    if not os.path.isdir(os.path.join(os.getcwd(), 'targetFiles')):
        print("targetFiles folder for files to be sent not created. Creating now...")
        time.sleep(1)
        try:
            os.mkdir(os.path.join(os.getcwd(), 'targetFiles'))
        except Exception as e:
            print("AN ERROR OCCURRED IN CREATING THE TARGETFILES FOLDER. ERROR: {}".format(e))
            print("Setup will exit...")
            sys.exit(1)
        print("Created targetFiles folder.")
    else:
        print("Found targetFiles folder. No need to create.")

    print()

    ### Check if csv file already exists ###
    if not os.path.isfile(os.path.join(os.getcwd(), 'emails.csv')):
        print("emails.csv file not found. Creating now (Please prepare your set of emails and target files, I will ask you for each entry you wish to add shortly)...")
        time.sleep(3)
        print()
        print()
        with open(os.path.join(os.getcwd(), 'emails.csv'), 'w') as f:
            print("""
If all your recipients have a common email domain, you can enter it now so that it will be automatically appended when you add the name.
For example, if you enter '@nass.moe.edu.sg' as a common email domain, Disseminator will add it automatically when it asks
you for the name of each recipient. For example, if you enter a recipient's name as 'Bob Alexander Arnold', the resultant
recipient email would be 'bob_alexander_arnold@nass.moe.edu.sg'.
            """)
            haveCommonDomain = input("Do all your recipient emails have a common email domain? (for e.g '@nass.moe.edu.sg') (y/n) ")
            print()
            print()
            if haveCommonDomain == 'y':
                allEntries = getEmailEntriesSmartVersion()
                print()
                print("Processing and writing entries....please wait!")
                time.sleep(1)
                print()
                f.write(convertDictToCSVString(allEntries))
                print("Created emails.csv file.")
            else:
                allEntries = getEmailEntriesFromUser()
                print()
                print("Processing and writing entries....please wait!")
                time.sleep(1)
                print()
                f.write(convertDictToCSVString(allEntries))
                print("Created emails.csv file.")
    else:
        print("Found emails.csv file. No need to create.")

    print()
    print("Setup successful! You may now run main.py to run the Disseminator program!")
    

