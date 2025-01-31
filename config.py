import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "+"