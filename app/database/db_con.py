import psycopg2

from app.config.config import settings
from app.logger.logger import logger


def get_db_connection():
	try:
		connection = psycopg2.connect(settings.DB_URL, sslmode='require')
		logger.debug('Database connection established')
		return connection
	except Exception:
		logger.exception('Could not connect to the database')
		raise

