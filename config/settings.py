import os
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Chronos")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # User Profile
    USER_NAME: str = os.getenv("USER_NAME", "Abdulrazaq Adeyemi")
    USER_EMAIL: str = os.getenv("USER_EMAIL", "hardexmarley340@gmail.com")
    USER_STUDENT_EMAIL: str = os.getenv("USER_STUDENT_EMAIL", "abdulrazaqaa.25@student.funaab.edu.ng")
    
    # Shift Math Anchor
    # 2026-10-20 was Day 1 of Morning Shift
    _anchor_raw = os.getenv("SHIFT_ANCHOR_DATE", "2026-10-20")
    try:
        SHIFT_ANCHOR_DATE: date = datetime.strptime(_anchor_raw, "%Y-%m-%d").date()
    except Exception:
        SHIFT_ANCHOR_DATE: date = date(2026, 10, 20)
        
    SHIFT_CYCLE_DAYS: int = int(os.getenv("SHIFT_CYCLE_DAYS", "9"))
    
    # Database
    DATABASE_PATH: Path = BASE_DIR / "database" / "chronos.db"
    
    # Email Radar
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
    
    # Web Push
    VAPID_PUBLIC_KEY: str = os.getenv("VAPID_PUBLIC_KEY", "")
    VAPID_PRIVATE_KEY: str = os.getenv("VAPID_PRIVATE_KEY", "")
    VAPID_ADMIN_EMAIL: str = os.getenv("VAPID_ADMIN_EMAIL", "mailto:hardexmarley340@gmail.com")

settings = Settings()
