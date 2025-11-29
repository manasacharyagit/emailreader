import imaplib

def login_imap(email, app_password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, app_password)
        mail.logout()
        return True
    except Exception as e:
        return False, str(e)