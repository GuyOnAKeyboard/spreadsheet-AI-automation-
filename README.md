# AI Spreadsheet Automation Agent (Google Sheets + Llama + Email)

An AI-powered spreadsheet automation agent that monitors Google Sheets, processes new data using a local LLM (Llama via Ollama), and automatically triggers actions like email notifications.

Turn your spreadsheet into an **intelligent workflow system** no manual checking, no repetitive summaries.

## Why This Project?

Manually checking spreadsheets, summarizing updates, and sending notifications is repetitive and time-consuming.

This project transforms your spreadsheet into an **AI-driven pipeline**:

- New data is detected automatically  
- AI understands and summarizes it  
- Actions (like emails) are triggered instantly  

Think of it as a lightweight, local alternative to **Zapier + AI**, but fully customizable and private.

## Features

**Automated Monitoring** - Continuously checks your Google Spreadsheet for new entries
**AI Summarization** - Uses local Llama AI (via Ollama) to generate intelligent summaries of new data
**Email Notifications** - Automatically sends summarized updates via email when new rows are detected
**Efficient Tracking** - Keeps track of the last processed row to avoid duplicate processing
**Secure Configuration** - Uses environment variables for sensitive data (API keys, credentials)

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.8+**
- **Ollama** - For running the local Llama model (download from [ollama.ai](https://ollama.ai))
- **Google API Key** - From [Google Cloud Console](https://console.cloud.google.com)
- **Gmail Account** - For sending email notifications (with App Password if 2FA is enabled)

## Installation

1. **Clone or download the repository**
   ```bash
   cd spreadSheet_Ai_automation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and start Ollama**
   - Download Ollama from [ollama.ai](https://ollama.ai)
   - Run: `ollama pull llama3.2:1b` (pulls the Llama 3.2 1B model)
   - Start Ollama service (usually runs on port 11434)

## Configuration

Create a `.env` file in the project root directory with the following variables:

```env
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here
SPREADSHEET_ID=your_spreadsheet_id_here
SHEET_NUMBER=Sheet1  # Name of the sheet to monitor

# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password_here
RECIPIENT_EMAIL=recipient@example.com
```

### Getting Your Google Spreadsheet ID

The spreadsheet ID is found in the URL:
```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0
```

### Getting Gmail App Password

1. Enable 2-Factor Authentication on your Google Account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Find "App Passwords" under Security
4. Generate a password for Gmail and use it as `SENDER_PASSWORD`

## Usage

Run the script in your terminal:

```bash
python main.py
```

### How It Works

1. **Fetches Data** - Connects to your Google Spreadsheet using the API
2. **Detects New Rows** - Compares current rows with the last processed row (stored in `last_row.txt`)
3. **AI Summarization** - If new rows are found:
   - Formats the new rows with headers
   - Sends them to the local Llama AI model for summarization
4. **Updates Tracking** - Records the total number of rows in `last_row.txt`
5. **Sends Email** - If new rows were detected, sends an email with the AI-generated summary

## Project Structure

```
spreadSheet_Ai_automation/
├── main.py                 # Main automation script
├── requirements.txt        # Python dependencies
├── last_row.txt           # Tracks the last processed row (auto-generated)
├── .gitignore             # Git ignore configuration
└── README.md              # This file
```

## Dependencies

- **google-api-python-client** - Google Sheets API access
- **langchain** - Framework for working with language models
- **langchain-ollama** - Ollama integration with LangChain
- **python-dotenv** - Environment variable management
- **langchain-google-genai** - Google AI integration (included)

## Troubleshooting

### "Failed to connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check if Ollama is accessible on `http://localhost:11434`

### "Authentication failed for Google API"
- Verify your `GOOGLE_API_KEY` is correct
- Ensure the API is enabled in Google Cloud Console

### "Gmail authentication failed"
- Use an App Password, not your regular Gmail password
- Verify `SENDER_EMAIL` and `SENDER_PASSWORD` are correct

### "No new data detected"
- Check if new rows have actually been added to the spreadsheet
- Verify `SPREADSHEET_ID` and `SHEET_NUMBER` are correct

## Future Enhancements

- [ ] Schedule runs using a task scheduler or cron job
- [ ] Support for multiple sheets
- [ ] Database integration for better row tracking
- [ ] Webhook support for custom integrations
- [ ] Custom AI prompt templates
- [ ] Dashboard for monitoring automation status

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, check the [Linkedin.](https://www.linkedin.com/in/guyonakeyboard/).
