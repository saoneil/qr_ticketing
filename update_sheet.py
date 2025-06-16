import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def update_sheet(df):
    
    # set up the google sheet
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\saone\\Documents\\python\\prod\\z.creds\\cloud_auth_json\\pma-fundraiser-5ec5ad28e215.json", scope)

    gc = gspread.authorize(creds)
    sheet = gc.open('Performance Taekwon-Do | Kitchen Party Fundraiser (Responses)').sheet1
        
    for index, row in df.iterrows():
        if row[4] == 'Y' and row[5] == None:
            sheet.update(f"F{index+1}", "Y")