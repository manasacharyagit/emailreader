import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


# from config import CREDS_PATH, TOKEN_PATH, SCOPES
CREDS_PATH = os.environ.get("CREDS_PATH")
TOKEN_PATH = os.environ.get("TOKEN_PATH")
SCOPES = os.environ.get("SCOPES").split(",")  # agar multiple scopes hain

def get_gmail_service():
    creds = None

    # 1️⃣ Load existing token (auto-login)
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2️⃣ If no token, or token expired → run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH, SCOPES
            )
            # creds = flow.run_local_server(port=8501, prompt='consent')
            creds = flow.run_console()


        # 3️⃣ Save new token
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    # 4️⃣ Build Gmail service
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)

    return service


