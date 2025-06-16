import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import time
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient import discovery


def send_tickets():
    creds = Credentials.from_service_account_file("C:\\Users\\saone\\Documents\\python\\prod\\z.creds\\cloud_auth_json\\pma-fundraiser-5ec5ad28e215.json")
    doc_id = "1UamPeyq3EpBsXeMfu6SkC2jq7vy7vo3s248t_FqJqPw"
    service = discovery.build('sheets', 'v4', credentials=creds)
    sheet_info = service.spreadsheets().get(spreadsheetId=doc_id).execute()
    sheet_range = sheet_info['sheets'][0]['properties']['title'] + '!A1:Z100'
    sheet = service.spreadsheets().values().get(spreadsheetId=doc_id,range=sheet_range).execute()
    rows = sheet['values']
    df = pd.DataFrame(rows)
    df = df.iloc[1: , :]
    
    directory = "C:\\Users\\saone\\Documents\\python\\prod\\qr_ticketing\\tickets"
    host = os.environ.get('email_host_python')
    username = os.environ.get('email_username_ptkd')
    password = os.environ.get('email_password_ptkd')       
        
        
    for filename in os.listdir(directory):
        if ", qr_sent.png" in filename:
            pass
        else:
            name, email, number = filename.split(", ")
            number = number.split(".png")[0]
            
            #Create the email subject, subject
            subject = f"Performance Taekwon-Do - Fundraiser Ticket - {name}, Admit {number}"
            bodystring = f"""Hello {name},
                \n\nAttached is your ticket to the Performance Taekwon-Do Kitchen Party Fundraiser in support of our athletes.
                \n\n\n\nThank you, and see you on Feb 4th at the Micmac Aquatic Club!"""

            # Create the email message
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = "performance_taekwondo@hotmail.com"
            msg["To"] = email
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
            
            new_filename = filename.replace(".png", ", qr_sent.png")     
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))