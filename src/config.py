from pathlib import Path
import os
from dotenv import load_dotenv

# ======================= ENVIRONMENT =======================
# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Path to the .env file
PATH_TO_ENV = BASE_DIR / ".env"

# Load environment variables from the .env file
load_dotenv(PATH_TO_ENV)

# Path to the resources directory
PATH_TO_RESOURCES = BASE_DIR / "src" / "resources"

# ======================= API KEYS =======================
# OpenAI API key loaded from environment variables
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Telegram Bot API key loaded from environment variables
TG_BOT_API_KEY = os.environ["TG_BOT_API_KEY"]
