import os
import streamlit as st
from openai import OpenAI

# --- Auth / client ---
# Prefer Streamlit Secrets. Fallback to env var.
api_key = None
if "openai_api_key" in st.secrets:
    api_key = st.secrets["openai_api_key"]
elif "OPENAI_API_KEY" in os.environ:
    api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key) if api_key else None

st.title("WhatsApp Copy Generator for Real Estate")
st.markdown("Craft tailored churn marketing messages for high-ticket real estate buyers.")

project_name = st.text_input("Project Name", value="ASBL Loft")

offer_summary = st.text_area(
    "Enter Offer Summary",
    value=(
        "Earn INR 85,000/month till Dec 2026 on a 1695 sft 3BHK with just INR 7.5L booking. "
        "Located in Financial District. Total price INR 1.84 Cr."
    ),
)

situation = st.selectbox(
    "Select Buyer Situation",
    [
        "Lead visited site but didn’t convert",
        "Lead showed initial interest, then went cold",
        "Buyer wants bigger unit (but Loft is 1695 sft)",
        "Investor missed booking window, may still be warm",
        "High-score CRM lead, hasn’t responded in 10 days",
        "Family buyer dropped off post cost sheet",
        "Generating New Lead",
        "Leads transitioned from new lead to not interested",
    ],
)

tone = st.selectbox(
    "Select Message Tone",
    [
        "Rational and Financial",
        "Scarcity and Urgency",
        "Gratitude and Emotional",
        "Reverse Psychology",
        "Direct and Assertive",
    ],
)

if st.button("Generate WhatsApp Message"):
    prompt = f"""
You are a highly experienced WhatsApp real estate marketing expert with decades of combined knowledge in buyer psychology and luxury sales.

Generate a churn marketing WhatsApp message for the following situation:
- Project: {project_name}
- Buyer Situation: {situation}
- Tone: {tone}
- Offer Summary: {offer_summary}

Constraints:
- Audience: INR 2Cr+ buyers who have likely seen the project before
- Style: smart, specific, emotionally resonant; avoid emojis; no fluff; use behavioral triggers
- Output: only the final WhatsApp message text
""".strip()

    if client is None:
        st.warning("Please set your OpenAI API key in Streamlit Secrets as 'openai_api_key' or set the OPENAI_API_KEY environment variable.")
    else:
        # v1 style call
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # pick a current chat model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        message = resp.choices[0].message.content
        st.text_area("Generated Message", value=message, height=250)
