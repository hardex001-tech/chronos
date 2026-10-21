from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database.db import get_connection
from core.scraper import scrape_url_metadata
from core.radar import check_email_radar

router = APIRouter(prefix="/api/apps", tags=["Applications"])

class UrlScrapeRequest(BaseModel):
    url: str

class ApplicationCreate(BaseModel):
    title: str
    company: str
    url: str
    logo_url: Optional[str] = None
    status: Optional[str] = "Applied"
    category: Optional[str] = "Job"
    applied_date: Optional[str] = None
    deadline_date: Optional[str] = None
    sender_domain: Optional[str] = None
    notes: Optional[str] = None

class StatusUpdate(BaseModel):
    status: str

@router.post("/scrape")
async def scrape_url(req: UrlScrapeRequest):
    """Scrapes page title, company, root domain, and logo from a pasted URL."""
    meta = await scrape_url_metadata(req.url)
    return meta

@router.get("")
def list_applications():
    """List all tracked applications and certifications."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, company, url, logo_url, status, category, applied_date, deadline_date, sender_domain, notes, created_at
        FROM applications
        ORDER BY id DESC;
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

@router.post("")
def create_application(app: ApplicationCreate):
    """Create a new tracked application/opportunity."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (title, company, url, logo_url, status, category, applied_date, deadline_date, sender_domain, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        app.title, app.company, app.url, app.logo_url, app.status,
        app.category, app.applied_date, app.deadline_date, app.sender_domain, app.notes
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": f"Successfully tracked {app.company}"}

@router.patch("/{app_id}/status")
def update_status(app_id: int, payload: StatusUpdate):
    """Update application lifecycle status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?;", (payload.status, app_id))
    conn.commit()
    conn.close()
    return {"message": "Status updated successfully"}

@router.delete("/{app_id}")
def delete_application(app_id: int):
    """Remove a tracked application."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?;", (app_id,))
    conn.commit()
    conn.close()
    return {"message": "Deleted successfully"}

@router.get("/radar/check")
def trigger_radar():
    """Run a scan for incoming recruiter emails."""
    alerts = check_email_radar()
    return {"alerts": alerts, "count": len(alerts)}
