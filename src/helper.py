import pymupdf as fitz
import fitz
import os
from dotenv import load_dotenv
from openai import OpenAI
from apify_client import ApifyClient
import google.generativeai as genai


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#client = OpenAI(api_key=OPENAI_API_KEY)
apify_client = ApifyClient(os.getenv("APIFY_TOKEN_KEY"))


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # ← rename to groq_client

def ask_openai(prompt, max_tokens=500):
    response = groq_client.chat.completions.create(  # ← use groq_client here
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
def extract_text_from_pdf(uploaded_file):

    doc = fitz.open(stream=uploaded_file.read(),filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


