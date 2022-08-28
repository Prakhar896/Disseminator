from email import message
import smtplib, ssl, re, os, subprocess, sys, shutil
import json, csv, datetime, time
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()

## Check dotenv file
if 'SenderEmailAppPassword' not in os.environ:
    print("SenderEmailAppPassword field not found in .env file. Please add it and try again.")
    sys.exit(1)
elif 'SenderEmail' not in os.environ:
    print("SenderEmail field not found in .env file. Please add it and try again.")
    sys.exit(1)
elif not os.path.isfile(os.path.join(os.getcwd(), 'emails.csv')):
    print("emails.csv file not found in current directory. Please add it and try again.")
    sys.exit(1)

### CSV FILE FORMAT ###
# email,file
# <email>,<file>

## Check if emails.csv file is empty
with open(os.path.join(os.getcwd(), 'emails.csv'), 'r') as f:
    reader = csv.reader(f)
    if not list(reader):
        print("emails.csv file is empty. Please add emails and try again.")
        sys.exit(1)

## Check if emails.csv file is valid
with open(os.path.join(os.getcwd(), 'emails.csv'), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2:
            print("emails.csv file is invalid. Please check the format and try again. (Invalid Row Length)")
            sys.exit(1)
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", row[0]):
            print("emails.csv file is invalid. Please check the format and try again. (Invalid Email)")
            sys.exit(1)
        elif not os.path.isfile(os.path.join(os.getcwd(), 'targetFiles', row[1])):
            print("emails.csv file is invalid. Please check the format and try again. (File Not Present In targetFiles Folder)")
            sys.exit(1)

######

## Confirm emails with user
print("----")
print("PLEASE CONFIRM THAT YOU INTEND TO SEND THE FILES TO THE FOLLOWING EMAILS:")
with open(os.path.join(os.getcwd(), 'emails.csv'), 'r') as f:
    reader = csv.reader(f)
    lineCount = 0
    for row in reader:
        lineCount += 1
        print("{}. Target Email: '{}', Target File: '{}'".format(lineCount, row[0], row[1]))
    print()
    print("Total of {} recipients.".format(lineCount))
print("----")

if input("Are you sure you want to continue? (y/n) ") != 'y':
    print("Setup will exit...")
    sys.exit(1)

## Ask for subject and text to attach to every email
subject = input("Please enter the subject of the email: ")
while True:
    if subject == '' or subject.strip() == '':
        print("Subject cannot be empty/have leading or trailing whitespaces. Please try again.")
        subject = input("Please enter the subject of the email: ")
        continue
    else:
        break
attachedText = None
if input("Would you like to add some text to all emails you send? (y/n) ") == 'y':
    attachedText = input("Please enter the text you would like to attach to every email: ")

print()
print("Connecting to email servers...")
time.sleep(2)

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.environ["SenderEmail"]
password = os.environ['SenderEmailAppPassword']

print("Initialising real time email logs...")
time.sleep(1)
print()
print("----")

## Send emails with respective file attached to it
with open(os.path.join(os.getcwd(), 'emails.csv'), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        receiver_email = row[0]
        file = row[1]

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            if attachedText is not None:
                msg.attach(MIMEText(attachedText))

            with open(os.path.join(os.getcwd(), 'targetFiles', file), 'rb') as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            
            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                "attachment; filename={}".format(secure_filename(file)),
            )
            msg.attach(part)

            # msg.attach(MIMEText(open(os.path.join(os.getcwd(), 'targetFiles', file), 'rb').read(), 'base64', 'utf-8'))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print("\n✅ Email sent to {}".format(receiver_email))
                time.sleep(1)
        except Exception as e:
            print("\n❌ ERROR OCCURRED IN SENDING FILE '{}' TO RECIPIENT '{}'. ERROR: {}".format(file, receiver_email, e))

print()
print("----")
print("Dissemination complete! Any potential errors in sending emails have been logged above.")