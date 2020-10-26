import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "info").lower()
LOG_HANDLER = os.getenv("LOG_HANDLER", "sys").lower()
