from flask import Flask
from dotenv import load_dotenv
from app.config.config import Config

load_dotenv()

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates'
            )
    app.config.from_object(Config)
    
    return app