from email.mime.text import MIMEText
import smtplib
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from email.mime.multipart import MIMEMultipart

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')
SHEET_NUMBER=os.getenv('SHEET_NUMBER')
SENDER_EMAIL=os.getenv('SENDER_EMAIL')
SENDER_PASSWORD=os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL=os.getenv('RECIPIENT_EMAIL')
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587

model=init_chat_model(
    model='llama3.2:1b',
    model_provider='ollama',
)

def summarize_with_ai(text):
    system_prompt="""
    You are a helful assistant that summarizes spreadsheet data.
    You will receive new rows that were added to a Google sreadsheet.
    Please Provide a clear, concise summary of this data. 
    The output should be very concise so someone reading could understand what happned in the spreadsheet,
    the output should always be in tabular format as user would provide you the new rows and headers
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

def send_email(subject,body):
    """Send email with summary"""
    
    msg=MIMEMultipart()
    msg['From']=SENDER_EMAIL
    msg['To']=RECIPIENT_EMAIL
    msg['Subject']=subject
    msg.attach(MIMEText(body,'plain'))
    
    server=smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL,SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"Email sent sucessfully to {RECIPIENT_EMAIL}")
    
if len(new_row)>0:
    send_email('Daily update info', ai_summary)
