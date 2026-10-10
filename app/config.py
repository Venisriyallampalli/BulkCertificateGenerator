
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")

MAX_RECIPIENTS = int(os.getenv("MAX_RECIPIENTS", "200"))
