import httpx
from datetime import date, datetime
from database.db import get_connection

async def sync_github_streak(username: str = "hardex001-tech") -> dict:
    """
    Check GitHub public events API to detect if user pushed code today.
    If yes, automatically increments the GitHub streak in Chronos.
    """
    url = f"https://api.github.com/users/{username}/events"
    today_iso = date.today().isoformat()

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, headers={"User-Agent": "Chronos-Sentinel/1.0"})
            if resp.status_code == 200:
                events = resp.json()
                # Check for PushEvent today
                has_pushed_today = False
                for ev in events:
                    if ev.get("type") == "PushEvent":
                        created_at = ev.get("created_at", "")
                        if created_at.startswith(today_iso):
                            has_pushed_today = True
                            break

                if has_pushed_today:
                    # Update database task
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE tasks
                        SET completed_today = 1, streak_count = streak_count + 1, last_completed = ?
                        WHERE title LIKE '%GitHub%' AND completed_today = 0;
                    """, (today_iso,))
                    conn.commit()
                    conn.close()
                    return {"synced": True, "pushed_today": True}
    except Exception:
        pass

    return {"synced": False, "pushed_today": False}

async def sync_tryhackme_streak(username: str) -> dict:
    """
    Check TryHackMe public profile for user's active streak count.
    """
    if not username:
        return {"synced": False}

    url = f"https://tryhackme.com/api/v2/public-profile?username={username}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, headers={"User-Agent": "Chronos-Sentinel/1.0"})
            if resp.status_code == 200:
                data = resp.json()
                streak = data.get("data", {}).get("streak", 0)
                if streak > 0:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE tasks
                        SET streak_count = ?, completed_today = 1
                        WHERE title LIKE '%TryHackMe%';
                    """, (streak,))
                    conn.commit()
                    conn.close()
                    return {"synced": True, "streak": streak}
    except Exception:
        pass

    return {"synced": False}
