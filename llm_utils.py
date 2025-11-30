from openai import OpenAI
from config import OPENROUTER_API_KEY


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def summarize_email(email_text):
    prompt = f"""
Summarize this email in 4–5 lines.
Classify it as: Scam / Important / Promotional / Neutral.
Describe the tone.

Email:
{email_text}
"""

    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",   # optional
            "X-Title": "Email-AI-Agent"           # optional
        },
        model="openai/gpt-4o-mini",   # correct OpenRouter model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content

def reply_mail(email_text):
    prompt = f"""
Suggest a reply to this mail to the user and keep all the cases in cosideration. For example if user 
want to reply in yes or affirmation suggest that version and if he wants to decline suggest that version too

Email: {email_text}

"""
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",   # optional
            "X-Title": "Email-AI-Agent"           # optional
        },

        model = "openai/gpt-4o-mini",
        messages=[{"role": "user", "content":prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content