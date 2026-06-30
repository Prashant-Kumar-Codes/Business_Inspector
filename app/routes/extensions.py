from flask import Blueprint, render_template, url_for, request, redirect, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import os
import sys
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from the .env file in the app directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

print('Inside extensions')

# connection with the database
def dbConn():
    try: 
        db_url = os.getenv('DB_URL')
        if not db_url:
            raise ValueError("DB_URL is not set in the environment variables.")
            
        parsed = urlparse(db_url)
        conn = psycopg2.connect(
            host = parsed.hostname,
            port = parsed.port or 5432,
            user = parsed.username,
            password = parsed.password,
            database = parsed.path.lstrip('/'),
            sslmode = 'require'
        )
        print(f'DB {parsed.username} - Connected')
        return conn

    except Exception as e:
        print(f'Error in connecting with Database: {e}')

dbConn()