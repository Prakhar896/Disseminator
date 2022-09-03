# Disseminator

Disseminator is a Python program which allows you to disseminate a bunch of unique files that are to be sent separately to multiple emails easily. Setting up and using Disseminator is a piece of cake! You can say goodbye to your days of constant dragging-and-dropping and hitting "Send".

## Table Of Contents

- [Usage](#usage)
    - [Requirements for Disseminator](#requirements-for-disseminator)
  - [Setting up](#setting-up)
    - [Preparing your Google Email Account](#preparing-your-google-email-account)
  - [Actually Setting up](#actually-setting-up)
- [Potential Errors](#potential-errors)
  - [File not Found](#file-not-found)
- [Adding/Deleting/Editing Recipient Records](#addingdeletingediting-recipient-records)
  - [Adding Recipient Records](#adding-recipient-records)
  - [Deleting Recipient Records](#deleting-recipient-records)
  - [Editing Recipient Records](#editing-recipient-records)

## Usage

---
#### Requirements for Disseminator
1) **>Python 3.8**, [Install Python Here](https://python.org)
2) Git Installation on Computer
---

Setting up Disseminator is super easy with the in-built `setup.py` file that sets up Disseminator for immediate use. Here are the steps to your first mass dissemination of files!

### Setting up

#### Preparing your Google Email Account

Unfortunately, at this time, Disseminator only works with sender emails that are Google Accounts due to OAuth limitations. You will need to do a few things to prepare your Google Account for Disseminator. **Ensure that the Google Account you intend to use to send emails has 2FA enabled. This is a requirement.**

1) Go to `myaccount.google.com`.

> This is the MyAccount portal to manage a Google Account user's account. Ensure you are logged into the portal with the account you intend to use.

2) Click "Security" in the sidebar.

3) Under "Signing in to Google", click "App Passwords" (will only show up if you have 2FA enabled).

<img width="720" alt="Screenshot 2022-08-28 at 2 18 56 PM" src="https://user-images.githubusercontent.com/53103894/187060542-33cf2a9d-8b62-4da8-87ba-0d66b0d5fa7b.png">

> ABOVE: What you should see after this step

4) Select "Custom" in the device dropdown and set the label to anything you want. (recommended is "Disseminator Program")

<img width="649" alt="Screenshot 2022-08-28 at 2 20 06 PM" src="https://user-images.githubusercontent.com/53103894/187060575-979349a3-efaf-4f8f-94a1-c92a9d44e455.png">

> ABOVE: Click the "Custom" label.

5) Click the blue "Generate" button. Copy your App Password at the top right. **You will need it later**

### Actually setting up

1) First, download the latest version package (under the `Releases` section) of Disseminator from GitHub onto your computer.

2) Next, open up your Terminal/CMD and run `setup.py` using Python. For e.g, run `python3 setup.py`.

> Read the on-screen text to learn more about what Setup is doing to prep the environment for the setup process. When run, Setup installs all the modules from the `requirements.txt` file just in case.

3) Type '1' to being setup processes.

<img width="679" alt="Screenshot 2022-08-28 at 2 23 57 PM" src="https://user-images.githubusercontent.com/53103894/187060671-cee5b573-e05c-48f1-8f9b-34a8bd9faf6b.png">

4) Enter the email address of the Google Account you intend to use (for which you just created the App Password) as well as the App Password when prompted for them respectively.

<img width="599" alt="Screenshot 2022-08-28 at 2 25 40 PM" src="https://user-images.githubusercontent.com/53103894/187060710-d9731fa6-83a6-447a-b568-03025903fad4.png">

5) If all the recipients you plan to send emails to have a common domain, you can enter it at the start (before entering each recipient's details) so that Disseminator will add the common domain at the back for you.

For example, if you type in the common domain `@nass.moe.edu.sg` at the start, Disseminator will simply ask you for the name of the recipient. Thus, when prompted later on for the recipient's name, when you put in `Bob Alexander Arnold` or `tom.cruise`, the resultant emails would be `bob_alexander_arnold@nass.moe.edu.sg` and `tom.cruise@nass.moe.edu.sg` respectively.

This makes your life easier when entering details in.

After saying `y`, you can enter in the common domain that all recipients share. For e.g, `@nass.moe.edu.sg`
> NOTE: It must start with an `@` sign.

**If your recipients do not have a common domain, do not say `y` when prompted by Setup.**

<img width="929" alt="Screenshot 2022-08-28 at 2 30 57 PM" src="https://user-images.githubusercontent.com/53103894/187060880-c4e1a1b4-235e-4610-87d5-591492fec4ea.png">

6) Enter the number of recipients you have.

This is the number of times Setup will ask you for recipient details.

<img width="701" alt="Screenshot 2022-08-28 at 2 31 35 PM" src="https://user-images.githubusercontent.com/53103894/187060899-1d461c51-afd6-4663-9c10-f99dd59d2002.png">

> ABOVE: What it would look like to enter the number of recipients if you *do* say `y` to the common domain prompt.

8) Dump all your files to distribute in the `targetFiles` folder in the root folder of Disseminator.

Ensure that there are no subfolders. There's no limitation to the filename or file type. There is a cap to the file size of 25MB however.

The folder should have been auto-generated by Setup when you typed `1` in step 3. The generation should also be displayed in text, so read the output carefully.

7) Enter all your recipients' details respectively.

If you said `y` to the common domain prompt, you may enter the person's name.

If not, please enter the recipient's full email address.

<img width="683" alt="Screenshot 2022-08-28 at 2 35 30 PM" src="https://user-images.githubusercontent.com/53103894/187061051-fbc91a29-652f-40c8-b0cf-78f71ec839c3.png">

> ABOVE: A series of prompts with responses from the user showing the inputting of recipient details.

8) Voila!

The setup process is complete! Now, you can begin to send emails!

### Sending Emails

Sending emails is quite straightforward. Here's the steps to operating the `main.py` file.

1) Run the `main.py` file in Terminal/CMD. For e.g, run `python3 main.py`

2) Confirm the recipient details. Type `y` if they are correct.

<img width="617" alt="Screenshot 2022-08-28 at 2 39 16 PM" src="https://user-images.githubusercontent.com/53103894/187061161-58310401-843a-4f5e-ae55-174fc518d3dc.png">

3) Enter the subject of your emails.

The subject will be the same for every single email sent.

<img width="376" alt="Screenshot 2022-08-28 at 2 43 10 PM" src="https://user-images.githubusercontent.com/53103894/187061273-5654b4ec-4f8a-4d0c-9603-f3da88aa6819.png">

4) If you would like to add some text to your emails, type `y` when prompted and type in the text. If not, type `n`.

Pro-tip: For further personalisation, in the text that you type in, you can type `{email}` anywhere in the text. That serves as a placeholder which will be replaced with the recipient's email who an email is being sent to.

For example, if you attach the text `Dear {email}, attached are top secret government secrets. Handle carefully.` and an email is sent to `tom.cruise@nass.moe.edu.sg`, the text in the email sent to that recipient will be `Dear tom.cruise@nass.moe.edu.sg, attached are top secret government secrets. Handle carefully.`

<img width="654" alt="Screenshot 2022-08-28 at 2 46 33 PM" src="https://user-images.githubusercontent.com/53103894/187061383-bb3f6c7e-3a3e-44b0-8528-b87ea9baaf35.png">

> ABOVE: A sample personalised text attachment to each email.

5) Sit back and wait.

After the previous step, Disseminator automatically begins the work fo sending out each email. The logs of each email are displayed in the Terminal/CMD output so read carefully. The emails are sent periodically. If an error occurs in sending any email, it will be displayed in the output, so read carefully.

Ideally, you should see a series of green ticks (✅ emojis) all the way through.

---

## Potential Errors

### File not Found

This error occurs when keying in recipient details in [Setup](#actually-setting-up). This is because the filename that you keyed in does not exist in the `targetFiles` folder. Please drop the file in before typing in the filename. You can do this while the target file prompt is open.


## Adding/Deleting/Editing Recipient Records

After setting up, all recipient records are stored in a CSV file (comma-separated values) called `emails.csv` at the root of the Disseminator folder.

Have a completely different recipient roster you wanna switch to? Simply delete the `emails.csv` file and run Setup again.

### Adding Recipient Records

To add a recipient record, simply, on a newline, type in their email, followed by a comma, followed by the name of the file (target file) to be sent to them.

For e.g, add `tom.cruise@gmail.com,tomCruiseMovie.MOV`. (Ensure there is no space on either sides of the comma)

https://user-images.githubusercontent.com/53103894/187061557-67679e8a-8530-4f57-9b62-b9a39bfdef46.mov

### Deleting Recipient Records

To delete a recipient record, simply remove the line from the `emails.csv` file. Ensure that there are no newlines in between records.

Example clip:

https://user-images.githubusercontent.com/53103894/187061596-1edc0aa9-166b-4cf2-bd62-a56b75eb144b.mov

### Editing Recipient Records

To edit a recipient record, simply go to their line and edit the value.

If you want to change their email, change the value before the comma. If not (you want to change their target file), change the value after the comma.

Ensure there is no spaces on either sides of the comma.

Example clip:

https://user-images.githubusercontent.com/53103894/187061667-6bdf976c-3bc7-4386-a6b7-51ad4a76c104.mov

---

And that's it for the documentation! Thank you for using Disseminator!!!

© 2022 Prakhar Trivedi
