from google.oauth2.service_account import Credentials
from googleapiclient import discovery
import qrcode
import pandas as pd
import os


def create_tickets():       
    creds = Credentials.from_service_account_file("C:\\Users\\saone\\Documents\\Python Stuff\\prod\\z.creds\\cloud_auth_json\\pma-fundraiser-5ec5ad28e215.json")
    doc_id = "1UamPeyq3EpBsXeMfu6SkC2jq7vy7vo3s248t_FqJqPw"

    service = discovery.build('sheets', 'v4', credentials=creds)

    # Get the range of cells in the sheet
    sheet_info = service.spreadsheets().get(spreadsheetId=doc_id).execute()
    sheet_range = sheet_info['sheets'][0]['properties']['title'] + '!A1:Z100'

    # Use the Sheets API to get the data in the sheet
    sheet = service.spreadsheets().values().get(
        spreadsheetId=doc_id,
        range=sheet_range
    ).execute()

    # The sheet data is returned as a list of rows, where each row is a list of cells
    rows = sheet['values']
    df = pd.DataFrame(rows)
    df = df.iloc[1: , :]
    timestamp_index, name_index, email_index, numtix_index, paid_index, qrsent_index = 0,1,2,3,4,5

    # Loop through the rows in the DataFrame
    for index, row in df.iterrows():
        # Check the values in the Paid and Email QR Sent columns
        if row[paid_index] == 'Y' and row[qrsent_index] == None:
            # Generate the QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"{row[name_index]}, {row[email_index]}, Admit {row[numtix_index]}")
            qr.make(fit=True)

            # Save the QR code as an image file
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"C:\\Users\\saone\\Documents\\Python Stuff\\prod\\qr_ticketing\\tickets\\{row[name_index]}, {row[email_index]}, {row[numtix_index]}.png")

    return df