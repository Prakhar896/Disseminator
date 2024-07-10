from email import message
import smtplib, ssl, re, os, sys, certifi
import csv, time
from activation import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()

def getPersonalisedText(text, email, name):
    # Email
    personalisedText = text.replace("{email}", receiver_email)

    # Email Domain Detached
    personalisedText = personalisedText.replace("{emailDomainDetached}", email.split('@')[0])

    # Name
    personalisedText = personalisedText.replace("{name}", name)

    # Custom
    if personalisedText.find("{custom}") != -1:
        custom = input("Please enter your custom text for recipient with email '{}': ".format(email))
        personalisedText = personalisedText.replace("{custom}", custom)

    return personalisedText

def createMessage(senderEmail, receiverEmail, msgSubject, emailText, name):
    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = receiverEmail
    msg['Subject'] = msgSubject


    if emailText is not None:
        personalisedText = getPersonalisedText(emailText, receiverEmail, name)
        msg.attach(MIMEText(personalisedText))

    # with open(os.path.join(os.getcwd(), 'targetFiles', attachedFilename), 'rb') as f:
    #     part = MIMEBase("application", "octet-stream")
    #     part.set_payload(f.read())
            
    # encoders.encode_base64(part)

    # part.add_header(
    #     "Content-Disposition",
    #     "attachment; filename={}".format(secure_filename(attachedFilename)),
    # )
    # msg.attach(part)

    return msg

## Check activation
activationCheck = checkForActivation()
if activationCheck == True:
    pass
elif activationCheck == False:
    print("This copy is not activated! Initializing copy activation...")
    print()
    version = None
    if not os.path.isfile(os.path.join(os.getcwd(), 'version.txt')):
        version = input("Please enter the version of Disseminator you are using: ")
        print()
    else:
        version = open('version.txt', 'r').read()
    
    try:
        initActivation("910a3w4m", version)
    except Exception as e:
        print("MAIN: An error occurred in copy activation. Error: {}".format(e))
        print("Aborting...")
        sys.exit(1)
else:
    print("This copy's license key needs to verified (every 14 days). Triggering key verification request...")
    print()
    version = None
    if not os.path.isfile(os.path.join(os.getcwd(), 'version.txt')):
        version = input("Please enter the version of Disseminator you are using: ")
        print()
    else:
        version = open('version.txt', 'r').read()
    try:
        makeKVR("910a3w4m", version)
    except Exception as e:
        print("MAIN: Failed to make key verification request. Error: {}".format(e))
        print("Aborting...")
        sys.exit(1)

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

emailsData = {}

with open(os.path.join(os.getcwd(), 'emails.csv'), 'r') as f:
    reader = csv.reader(f)

    tempData = list(reader)

    ## Check if emails.csv file is empty
    if not tempData:
        print("emails.csv file is empty. Please add emails and try again.")
        sys.exit(1)

    ## Check if emails.csv file is valid
    for row in tempData:
        if len(row) < 2:
            print("emails.csv file is invalid. Please check the format and try again. (Invalid Row Length)")
            sys.exit(1)
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", row[0]):
            print("emails.csv file is invalid. Please check the format and try again. (Invalid Email)")
            sys.exit(1)
        # elif not os.path.isfile(os.path.join(os.getcwd(), 'targetFiles', row[1])):
        #     print("emails.csv file is invalid. Please check the format and try again. (File Not Present In targetFiles Folder)")
        #     sys.exit(1)
        else:
            emailsData[row[0]] = row[1]

######

## Confirm emails with user
print("----")
print("PLEASE CONFIRM THAT YOU INTEND TO SEND TO THE FOLLOWING EMAILS:")
lineCount = 0
for email in emailsData:
    lineCount += 1
    print("{}. Target Email: '{}', Name: '{}'".format(lineCount, email, emailsData[email]))
print()
print("Total of {} recipients.".format(lineCount))
print("----")

if input("Are you sure you want to continue? (y/n) ") != 'y':
    print("Disseminator will exit...")
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
    if attachedText == "!file":
        print()
        print("Creating msg.txt file for long message...")
        time.sleep(1)
        print()
        try:
            with open(os.path.join(os.getcwd(), 'msg.txt'), 'w') as f:
                if sys.platform == "darwin":
                    os.system("open -a TextEdit {}".format(os.path.join(os.getcwd(), 'msg.txt')))
            
                print("Disseminator just created a file called 'msg.txt' in the root of the Disseminator folder; please open it and enter your long message in the file.")
                print("When you are done, save the file and close it.")
                input("Press Enter to continue when closed...")

            with open(os.path.join(os.getcwd(), 'msg.txt'), 'r') as f:
                attachedText = f.read()
            
            ## Delete msg.txt file
            os.remove(os.path.join(os.getcwd(), 'msg.txt'))
        except Exception as e:
            print("An error occurred while trying to create/get message from/delete msg.txt file. Please try again. Error: {}".format(e))
            sys.exit(1)

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
context = ssl.create_default_context(cafile=certifi.where())
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)

    for receiver_email in emailsData:
        try:
            msg = createMessage(sender_email, receiver_email, subject, attachedText, emailsData[receiver_email])
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("\n✅ Email sent to {}".format(receiver_email))
            time.sleep(1)
        except Exception as e:
            print("\n❌ ERROR OCCURRED IN SENDING FILE '{}' TO RECIPIENT '{}'. ERROR: {}".format(emailsData[receiver_email], receiver_email, e))

print()
print("----")
print("Dissemination complete! Any potential errors in sending emails have been logged above.")