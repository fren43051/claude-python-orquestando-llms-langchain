import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL_NAME = os.getenv("CLAUDE_MODEL_NAME")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME")