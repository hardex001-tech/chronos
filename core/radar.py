import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any
from config.settings import settings
from database.db import get_connection

def check_email_radar() -> List[Dict[str, Any]]:
    """
    Quietly check user's Gmail inbox for messages from tracked company domains.
    Returns list of matches. Leaves emails UNREAD.
    """
    if not settings.GMAIL_USER or not settings.GMAIL_APP_PASSWORD:
        return []

    # Get active tracked domains from database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT company, sender_domain FROM applications WHERE sender_domain IS NOT NULL AND sender_domain != '';")
    rows = cursor.fetchall()
    conn.close()

    domain_map = {row["sender_domain"].lower(): row["company"] for row in rows}
    if not domain_map:
        return []

    detected_alerts = []

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(settings.GMAIL_USER, settings.GMAIL_APP_PASSWORD)
        mail.select("INBOX", readonly=True)  # READ ONLY ensures zero state changes

        # Search for UNSEEN messages
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            mail.logout()
            return []

        email_ids = messages[0].split()
        # Check only the most recent 15 unread emails for performance
        for e_id in email_ids[-15:]:
            status, msg_data = mail.fetch(e_id, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_hdr = msg.get("From", "")
                    subject_hdr = msg.get("Subject", "(No Subject)")

                    # Decode subject
                    decoded_subj = ""
                    for sub, enc in decode_header(subject_hdr):
                        if isinstance(sub, bytes):
                            decoded_subj += sub.decode(enc or "utf-8", errors="ignore")
                        else:
                            decoded_subj += str(sub)

                    # Match against domain map
                    from_lower = from_hdr.lower()
                    for domain, company in domain_map.items():
                        if domain in from_lower:
                            detected_alerts.append({
                                "company": company,
                                "domain": domain,
                                "sender": from_hdr,
                                "subject": decoded_subj,
                                "alert_message": f"New update from {company}: '{decoded_subj}'"
                            })
                            break

        mail.logout()
    except Exception as e:
        # Fails gracefully if offline or no credentials configured
        pass

    return detected_alerts
