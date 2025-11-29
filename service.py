from bs4 import BeautifulSoup
import base64

def get_user_email(service):
    profile = service.users().getProfile(userId='me').execute()
    return profile.get("emailAddress", None)


def list_emails(service, max_results=100):
    # service = get_gmail_service() se mila Gmail client
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id'], format='metadata', 
            metadataHeaders=['From','Subject','Date']
        ).execute()

        headers = msg_data['payload']['headers']
        email_dict = {h['name']: h['value'] for h in headers}
        email_dict['id'] = msg['id']   # ← add message id
        email_list.append(email_dict)

    return email_list





def get_email_content(service, msg_id):
    message = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    
    parts = message["payload"].get("parts", [])
    email_body = ""

    # extract HTML body
    for part in parts:
        if part["mimeType"] == "text/html":
            data = part["body"]["data"]
            decoded = base64.urlsafe_b64decode(data).decode("utf-8")
            soup = BeautifulSoup(decoded, "html.parser")
            email_body = soup.get_text(separator="\n")   # 🔥 convert to plain text
            break

        if part["mimeType"] == "text/plain":
            data = part["body"]["data"]
            decoded = base64.urlsafe_b64decode(data).decode("utf-8")
            email_body = decoded
            break

    return email_body

