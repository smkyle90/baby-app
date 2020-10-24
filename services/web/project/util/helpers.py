"""App helper functions
"""
import os
import random
import smtplib
import ssl
import subprocess
from email.mime.text import MIMEText

import requests

"""
https://pthree.org/2012/01/07/encrypted-mutt-imap-smtp-passwords/
https://gist.github.com/bnagy/8914f712f689cc01c267
"""

def send_email(receiver_email, subject, html):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "1993oad@gmail.com"  # Enter your address
    password = os.environ["OADPW"]
    message = "Subject: {}\n\n{}".format(subject, html)
    msg = MIMEText(message, "html")
    msg['Subject'] = subject
    msg['From'] = sender_email

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
