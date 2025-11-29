import streamlit as st
import openai

# ----------- OPENROUTER CONFIG -----------
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"
# -----------------------------------------


# ----------- SUMMARY FUNCTION -----------
def summarize_email(email_text):
    prompt = f"""
Summarize this email in 4–5 lines.
Classify it as: Scam / Important / Promotional / Neutral.
Describe the tone.

Email:
{email_text}
"""

    response = openai.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Email-AI-Agent"
        }
    )

    return response.choices[0].message["content"]


# ----------- REPLY FUNCTION -----------
def reply_mail(email_text):
    prompt = f"""
Suggest multiple possible replies to this mail:
1. If user wants to accept/agrees → give version.
2. If user wants to decline → give version.
3. If user wants neutral clarification → give version.

Email:
{email_text}
"""

    response = openai.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Email-AI-Agent"
        }
    )

    return response.choices[0].message["content"]
