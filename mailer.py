import smtplib, ssl
import sys
import json

PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "" 
SENDER_EMAIL_PASSWORD = ""

emotions = ["angry", "disgust", "fear", "sad", "surprise", "neutral"]

def compose_message(output_dic):
    msgs = [f"""
    Hello! Here is a summary of how you did just now:

    You spoke around {output_dic["AVG_SPEECH_RATE"]} words per minute.
    You said the following illegal words: {output_dic["SAID_ILLEGALS"]}.
    Your dominant expression was {max(output_dic["MOOD"].keys(), key=lambda x: output_dic["MOOD"][x])}.
    
    Thank you for using 6UAssist!
    \n"""]
    lines = [f"\
            6-UAssist\n", "Subject: Here is your performance summary.\n"] + msgs
    return "".join(lines)

def send_message(message, RECEIVER_EMAILS, SENDER_EMAIL_PASSWORD=SENDER_EMAIL_PASSWORD):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        for receiver_email in RECEIVER_EMAILS:
            server.sendmail(SENDER_EMAIL, receiver_email, message)