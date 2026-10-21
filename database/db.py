import sqlite3
from pathlib import Path
from config.settings import settings

def get_connection():
    """Return a sqlite3 connection with dictionary row factory."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed with active trackers."""
    Path(settings.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        url TEXT NOT NULL,
        logo_url TEXT,
        status TEXT DEFAULT 'Applied',
        category TEXT DEFAULT 'Job',
        applied_date TEXT,
        deadline_date TEXT,
        sender_domain TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. Tasks / Streaks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT DEFAULT 'Streak',
        streak_count INTEGER DEFAULT 0,
        completed_today INTEGER DEFAULT 0,
        last_completed TEXT,
        target_link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 3. Push Subscriptions (for Samsung S21)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS push_subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT UNIQUE NOT NULL,
        p256dh TEXT NOT NULL,
        auth TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Seed default applications if empty
    cursor.execute("SELECT COUNT(*) FROM applications;")
    if cursor.fetchone()[0] == 0:
        seed_apps = [
            ("Huawei ICT Competition 2026-2027", "Huawei", "https://e.huawei.com/en/talent/", "https://www.huawei.com/favicon.ico", "Ongoing", "Competition", "2026-10-07", "2026-11-30", "huawei.com", "Network Track (HCIA-Datacom). Prelim exam late Nov."),
            ("Microsoft Learn Student Ambassadors", "Microsoft", "https://mvp.microsoft.com/studentambassadors", "https://www.microsoft.com/favicon.ico", "Under Review", "Fellowship", "2026-10-07", "2026-11-15", "microsoft.com", "Quarterly batch review. Joined official Discord."),
            ("Google Cloud Cybersecurity (Mentor Me)", "Mentor Me Collective", "https://mentormecollective.org", "", "In Progress", "Certification", "2026-10-10", "2026-11-20", "mentormecollective.org", "Active class cohort. Working on OSINT and Cloud Security modules."),
            ("AWS Educate Student Portal", "Amazon Web Services", "https://www.awseducate.com", "https://a0.awsstatic.com/main/images/site/fav/favicon.ico", "Active", "Certification", "2026-10-17", "2026-11-15", "amazon.com", "Cloud Computing 101 badge enrolled.")
        ]
        cursor.executemany("""
            INSERT INTO applications (title, company, url, logo_url, status, category, applied_date, deadline_date, sender_domain, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, seed_apps)
        
    # Seed default tasks / streaks if empty (Start all streaks at 0 clean)
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    if cursor.fetchone()[0] == 0:
        seed_tasks = [
            ("TryHackMe 1 Room Streak", "Streak", 0, 0, None, "https://tryhackme.com"),
            ("Mentor Me Collective Google Cloud Lab", "Certification", 0, 0, None, "https://coursera.org"),
            ("FUNAAB Lecture Notes Revision (30 mins)", "University", 0, 0, None, None),
            ("Check SANS & Outreachy Portal Updates", "Career", 0, 0, None, "https://sans.edu")
        ]
        cursor.executemany("""
            INSERT INTO tasks (title, category, streak_count, completed_today, last_completed, target_link)
            VALUES (?, ?, ?, ?, ?, ?);
        """, seed_tasks)
        
    conn.commit()
    conn.close()
