import os
from dotenv import load_dotenv

load_dotenv(f".env")


def getenv(key: str, default="") -> str:
  return os.getenv(key, default)
