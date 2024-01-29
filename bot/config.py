import os
from dotenv import load_dotenv
import logging
import json

from bot.stress_data import StressData


# Get environment settings from .env file
load_dotenv()
TOKEN = os.getenv("SECRET_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

stress_data = StressData.from_file("data/raw.txt")
