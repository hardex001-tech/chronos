from fastapi import APIRouter
from pydantic import BaseModel
from database.db import get_connection
from core.notifier import send_push_notification

router = APIRouter(prefix="/api/push", tags=["Push Notifications"])

class SubscriptionPayload(BaseModel):
    endpoint: str
    keys: dict

@router.post("/subscribe")
def register_subscription(sub: SubscriptionPayload):
    """Store Web Push subscription from Samsung S21 or browser."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO push_subscriptions (endpoint, p256dh, auth)
        VALUES (?, ?, ?)
        ON CONFLICT(endpoint) DO UPDATE SET
            p256dh = excluded.p256dh,
            auth = excluded.auth;
    """, (sub.endpoint, sub.keys.get("p256dh", ""), sub.keys.get("auth", "")))
    conn.commit()
    conn.close()
    return {"status": "subscribed"}

@router.post("/test")
def test_alert():
    """Trigger a live test notification to the device."""
    send_push_notification(
        title="⚡ Chronos Test Alert",
        body="Chronos Push Sentinel is active on your device! Your shifts & deadlines are locked in.",
        url="/"
    )
    return {"message": "Test notification dispatched"}
