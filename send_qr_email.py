import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import time


def send_tickets():
    directory = "C:\\Users\\saone\\Documents\\Python Stuff\\prod\\qr_ticketing\\tickets"
    host = os.environ.get('email_host_python')
    username = os.environ.get('email_username_ptkd')
    password = os.environ.get('email_password_ptkd')

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        # Parse the file name to get the name, email, and number
        name, email, number = filename.split(", ")
        number = number.split(".png")[0]

        # Create the email subject
        subject = f"Performance Taekwon-Do - Fundraiser Ticket - {name}, Admit {number}"

        # Create the email body
        bodystring = f"""Hello {name},
            \n\nAttached is your ticket to the Performance Taekwon-Do Kitchen Party Fundraiser in support of our athletes.
            \n\n\n\nThank you, and see you on Feb 4th at the Micmac Aquatic Club!"""

        # Create the email message
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = "performance_taekwondo@hotmail.com"
        msg["To"] = email

        # Add the email body to the email message
        msg.attach(MIMEText(bodystring, "plain"))

        # Open the file and add it to the email message as an attachment
        with open(os.path.join(directory, filename), "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)

        with imaplib.IMAP4_SSL(host) as c:
                c.login(username, password)
                c.append('DRAFTS', '',
                    imaplib.Time2Internaldate(time.time()),
                    str(msg).encode('utf-8'))