import os
from dotenv import load_dotenv
load_dotenv()

APP_URL="https://www.saucedemo.com"
USER_NAME="standard_user"
USER_PASSWORD="secret_sauce"
LLM_MODEL="gpt-4o"
LLM_MODEL_TEMPERATURE=0.4
SCREENSHOT_DIR="screenshots"
LLM_PROVIDER="openai"  # or "local" for local models
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
BASE_URL="https://api.openai.com/v1"
LOG_LEVEL="INFO"
LOG_DIR="logs"
SCREENSHOT_DIR="screenshots"
PERF_BENCHMARK=True
