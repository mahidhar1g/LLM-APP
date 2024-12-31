import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API keys and configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = os.getenv("EMAIL_PORT")
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
# WHATSAPP_TO = os.getenv("WHATSAPP_TO")
