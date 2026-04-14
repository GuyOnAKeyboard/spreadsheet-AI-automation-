from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')
SHEET_NUMBER=os.getenv('SHEET_NUMBER')

def get_spreadsheet_data():
    """Fetch spreadsheet data"""
    
    service=build('sheets','v4',developerKey=GOOGLE_API_KEY)
    all_rows=service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NUMBER).execute()['values']
    
    with open('last_row.txt') as file:
        last_row=int(file.read())
    
    new_row=all_rows[last_row:]
    
    return all_rows,new_row


def update_last_row():
    """Fetch spreadsheet data and update last_row.txt"""
    all_rows, new_row = get_spreadsheet_data()
    total_rows = len(all_rows)
    
    with open('last_row.txt', 'w') as file:
        file.write(str(total_rows))
    
    return all_rows, new_row, total_rows

all_rows, new_row, total_rows = update_last_row()

print('All rows:',all_rows)
print('New rows:',new_row)
print('total rows:',total_rows)

