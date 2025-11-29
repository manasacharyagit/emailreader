import os
import json
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    # 1️⃣ Load credentials if already stored in session
    if "google_token" in st.session_state:
        creds = Credentials.from_authorized_user_info(
            st.session_state.google_token,
            SCOPES
        )
        return build('gmail', 'v1', credentials=creds)

    # 2️⃣ Setup OAuth Flow using Streamlit Secrets
    client_config = {
        "web": {
            "client_id": st.secrets["GCP_CLIENT_ID"],
            "client_secret": st.secrets["GCP_CLIENT_SECRET"],
            "auth_uri": st.secrets["GCP_AUTH_URI"],
            "token_uri": st.secrets["GCP_TOKEN_URI"],
            "redirect_uris": [ st.secrets["GCP_REDIRECT_URI"] ]
        }
    }

    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES,
        redirect_uri=st.secrets["GCP_REDIRECT_URI"]
    )

    auth_url, _ = flow.authorization_url(prompt="consent")

    st.markdown(f"[👉 Click here to login with Google]({auth_url})")

    # 3️⃣ Catch Google OAuth redirect in Streamlit
    code = st.query_params.get("code")

    if code:
        flow.fetch_token(code=code)
        creds = flow.credentials

        # Save token in Streamlit session
        st.session_state.google_token = json.loads(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    return None
