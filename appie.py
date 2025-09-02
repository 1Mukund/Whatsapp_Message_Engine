
import streamlit as st
import openai

# Set your OpenAI API key here or use st.secrets
openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else ""

st.title("WhatsApp Copy Generator for Real Estate")

st.markdown("Craft tailored churn marketing messages for high-ticket real estate buyers.")

project_name = st.text_input("Project Name", value="ASBL Loft")
offer_summary = st.text_area("Enter Offer Summary", value="Earn INR 85,000/month till Dec 2026 on a 1695 sft 3BHK with just INR 7.5L booking. Located in Financial District. Total price INR 1.84 Cr.")

situation = st.selectbox("Select Buyer Situation", [
    "Lead visited site but didn’t convert",
    "Lead showed initial interest, then went cold",
    "Buyer wants bigger unit (but Loft is 1695 sft)",
    "Investor missed booking window, may still be warm",
    "High-score CRM lead, hasn’t responded in 10 days",
    "Family buyer dropped off post cost sheet",
])

tone = st.selectbox("Select Message Tone", [
    "Rational and Financial",
    "Scarcity and Urgency",
    "Gratitude and Emotional",
    "Reverse Psychology",
    "Direct and Assertive",
])

if st.button("Generate WhatsApp Message"):
    prompt = f"""
You are a highly experienced WhatsApp real estate marketing expert with over 60 years of combined knowledge in buyer psychology and luxury sales.

Generate a churn marketing WhatsApp message for the following situation:
- Project: {project_name}
- Buyer Situation: {situation}
- Tone: {tone}
- Offer Summary: {offer_summary}

The message should be smart, emotionally resonant, avoid emojis, and be tailored to INR 2Cr+ buyers who have likely seen the project before. No fluff, focus on behavioral triggers.
"""

    if not openai.api_key:
        st.warning("Please set your OpenAI API key in Streamlit secrets to use this feature.")
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        message = response['choices'][0]['message']['content']
        st.text_area("Generated Message", value=message, height=250)
