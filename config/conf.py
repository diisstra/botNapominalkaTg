import os
from dotenv import load_dotenv

class Settings():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

settings = Settings()