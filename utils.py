import os
import smtplib, ssl

DATA_FILENAME = "data_tmp"

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "my@gmail.com"  # Enter your address
password = input("Type sender_email password and press enter: ")

# message = """\
# Subject: Hi there

# This is an example message."""


def clean_tmps():
    pass

def get_data(filename):
    pass

def record_data(filename):
    pass

def compile_message(filename):
    pass

def send_emails(filename, emails=[]):
    # TODO allow unsecure apps to run in sender email. Otherwise, this won't work
    # unless we use OAuth2
    message = compile_message(filename)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        for receiver_email in emails:
            server.sendmail(sender_email, receiver_email, message)