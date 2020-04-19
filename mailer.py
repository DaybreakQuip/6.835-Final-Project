import smtplib, ssl
import sys

PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "" 
RECEIVER_EMAILS = [""]
SENDER_EMAIL_PASSWORD = ""
CAN_SEND_EMAIL = False

def compose_message():
    msgs = ["""
    Hello! Here is a summary of how you did just now:

    You spoke on average _____.
    You said the following illegal words: _________.
    You are mostly __________.
    
    Thank you for using 6UAssist!
    \n"""]
    lines = [f"\
            6-UAssist\n", "Subject: Here is your performance summary.\n"] + msgs
    return "".join(lines)

def send_message(message, SENDER_EMAIL_PASSWORD=SENDER_EMAIL_PASSWORD):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        for receiver_email in RECEIVER_EMAILS:
            server.sendmail(SENDER_EMAIL, receiver_email, message)