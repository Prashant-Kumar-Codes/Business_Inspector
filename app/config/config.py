import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the app directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # database configuration
    DB_URL = os.getenv('DB_URL')
    

    # chatbot
    AI_KEY = os.getenv('AI_KEY')
    