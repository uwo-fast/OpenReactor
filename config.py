import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key"
    DATABASE_PATH = os.path.join(basedir, "openreactor.db")
    # Add other configuration variables as needed
