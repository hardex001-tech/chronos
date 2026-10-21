import json
from typing import Dict, Any
from database.db import get_connection
from config.settings import settings

try:
    from pywebpush import webpush, WebPushException
    WEBPUSH_AVAILABLE = True
except ImportError:
    WEBPUSH_AVAILABLE = False

def send_push_notification(title: str, body: str, url: str = "/", tag: str = "chronos-alert"):
    """
    Dispatch a Web Push notification to all registered client devices (Samsung S21, etc.).
    """
    payload = json.dumps({
        "title": title,
        "body": body,
        "icon": "/static/icons/icon-192.png",
        "badge": "/static/icons/icon-192.png",
        "url": url,
        "tag": tag
    })

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT endpoint, p256dh, auth FROM push_subscriptions;")
    subscriptions = cursor.fetchall()
    conn.close()

    if not subscriptions:
        print(f"[Push Notifier] No registered push subscriptions. Alert: {title} - {body}")
        return

    if not WEBPUSH_AVAILABLE or not settings.VAPID_PRIVATE_KEY:
        print(f"[Push Notifier Mock] {title}: {body}")
        return

    vapid_claims = {
        "sub": settings.VAPID_ADMIN_EMAIL
    }

    for sub in subscriptions:
        sub_info = {
            "endpoint": sub["endpoint"],
            "keys": {
                "p256dh": sub["p256dh"],
                "auth": sub["auth"]
            }
        }
        try:
            webpush(
                subscription_info=sub_info,
                data=payload,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims=vapid_claims
            )
        except Exception as e:
            # If subscription expired/unregistered, cleanup can happen here
            print(f"[Push Notifier] Error sending to {sub['endpoint'][:30]}...: {e}")
