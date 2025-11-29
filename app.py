from auth import get_gmail_service
import streamlit as st
from service import list_emails, get_email_content, get_user_email
from llm_utils import summarize_email, reply_mail
import pyperclip
st.set_page_config(layout="wide")

@st.cache_data(show_spinner=False)
def cached_list_emails(user_email):
    return list_emails(st.session_state.service)


# Initialize session states
if 'service' not in st.session_state:
    st.session_state.service = None

if 'user_email' not in st.session_state:
    st.session_state.user_email = None


if st.session_state.service is None:
    if st.button("Login with Google"):
        st.session_state.service = get_gmail_service()
        st.session_state.user_email = get_user_email(st.session_state.service)
        st.success("Login successful!")
        st.rerun()  # 🔥 force refresh UI
else:
    st.write(f"### Welcome, **{st.session_state.user_email}** 👋")
    if st.button("Log Out"):
        st.session_state.service = None
        st.rerun()  # logout ke baad bhi refresh


    
if st.session_state.service:
    emails = cached_list_emails(st.session_state.user_email)
    

    
    # Divide screen into 2 columns
    col1, col2 = st.columns([1, 2])  # col1: email list, col2: content

    with col1:
        st.subheader("Inbox")
        for i, email in enumerate(emails):
            if st.button(f"{email['Subject']} | {email['Date']}", key=f"email_{i}"):
                st.session_state.selected_email = get_email_content(st.session_state.service, email['id'])

    with col2:
        st.subheader("Email Content")
        
        if 'selected_email' in st.session_state and st.session_state.selected_email:
            # st.text_area("", st.session_state.selected_email, height=400)
            st.info(st.session_state.selected_email)

            # Summarize button
            if st.button("Summarize Email"):
                st.session_state.summary = summarize_email(st.session_state.selected_email)

            # Display summary if exists
            if 'summary' in st.session_state and st.session_state.summary:
                st.markdown("**Summary & Analysis:**")
                st.info(st.session_state.summary)

            # Suggest reply button
            if st.button("Suggest a reply"):
                st.session_state.reply = reply_mail(st.session_state.selected_email)

            # Display reply in editable box and copy button
            if 'reply' in st.session_state and st.session_state.reply:
                st.text_area("Suggested Reply (you can edit this too)", value=st.session_state.reply, height=350)

                import pyperclip
                if st.button("Copy Reply"):
                    pyperclip.copy(st.session_state.reply)
                    st.success("Copied to clipboard!")

                st.info(st.session_state.reply)

        else:
            st.info("Select an email to view its content")




