import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    if ENVIRONMENT == "production":
        MODEL_NAME = "gpt-4.1-nano"
    else:
        MODEL_NAME = "gpt-4.1-nano"

settings = Settings()