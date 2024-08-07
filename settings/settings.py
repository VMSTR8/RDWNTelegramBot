import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

DATABASE_URL = os.environ.get('DATABASE_URL')

TELEGRAM_GROUP_ID = os.environ.get('TELEGRAM_GROUP_ID')
