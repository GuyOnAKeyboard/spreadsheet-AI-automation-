from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')
SHEET_NUMBER=os.getenv('SHEET_NUMBER')

model=init_chat_model(
    model='llama3.2:1b',
    model_provider='ollama',
)

def summarize_with_ai(text):
    system_prompt="""
    You are a helful assistant that summarizes spreadsheet data.
    You will receive new rows that were added to a Google sreadsheet.
    Please Provide a clear, concise summary of this data. 
    The output should be very concise so someone reading could understand what happned in the spreadsheet
    """
    message=[{"role":"system", "content":system_prompt},
             {"role":"user", "content": f"Here are the new rows from the spreadsheet \n {text}"}]
    
    response=model.invoke(message).content
    
    return response


def get_spreadsheet_data():
    """Fetch spreadsheet data"""
    
    service=build('sheets','v4',developerKey=GOOGLE_API_KEY)
    all_rows=service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NUMBER).execute()['values']
    
    with open('last_row.txt') as file:
        last_row=int(file.read())
    
    new_row=all_rows[last_row:]
    headers=all_rows[0]
    
    return all_rows,new_row,headers


def update_last_row():
    """Fetch spreadsheet data and update last_row.txt"""
    all_rows, new_row,headers = get_spreadsheet_data()
    total_rows = len(all_rows)
    
    message_to_ai=f"Headers:{headers} \n New Rows: {new_row}"
    
    ai_summary=summarize_with_ai(message_to_ai)
    
    with open('last_row.txt', 'w') as file:
        file.write(str(total_rows))
    
    return all_rows, new_row, total_rows, ai_summary

all_rows, new_row, total_rows, ai_summary = update_last_row()

print('All rows:',all_rows)
print('New rows:',new_row)
print('total rows:',total_rows)
print('AI summary:',ai_summary)

