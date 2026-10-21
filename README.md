# ⚡ Chronos — Master of Time

> **Shift-Adaptive Career & Cybersecurity Sentinel**  
> An autonomous life operating system designed for shift workers, STEM undergraduates, and developers. Built with Python (FastAPI), SQLite, and Progressive Web App (PWA) architecture.

---

## 🌟 Why Chronos?
Most productivity apps assume a rigid 9-to-5 Monday–Friday schedule. For rotational shift workers and busy university students, this causes burnout and missed deadlines. 

**Chronos** aligns your 24-hour daily routine dynamically to your biological circadian rhythm across a **3 Morning / 3 Night / 3 Off** rotation, keeps your cybersecurity certifications on track, automatically scrapes metadata from job/fellowship URLs, and watches your email inbox for recruiter replies.

---

## 🚀 Core Features

* **Circadian Shift Engine (3-3-3):** Automatically calculates your current cycle day and delivers energy-appropriate daily agendas (Light Maintenance vs. Recovery vs. Deep Work Power Days).
* **Smart URL Metadata Scraping:** Paste any job, scholarship, or fellowship link (e.g. SANS, Goldman Sachs, Huawei, Coursera). Chronos extracts the title, company name, logo, and root domain in seconds.
* **Email Radar Sentinel (IMAP):** Quietly monitors incoming emails for replies from tracked employers/programs without reading personal messages.
* **Progressive Web App (PWA):** Installable as a standalone app on Android (Samsung Galaxy S21) and iOS with zero address bar and full mobile responsiveness.
* **Web Push & Sound Alarms:** Native mobile push notifications and break reminders that reach your phone even if your PC is turned off.
* **Daily Streaks Tracker:** Real-time tracking for TryHackMe labs, Google Cloud security exercises, and university lecture reviews.

---

## 🛠️ Architecture & Tech Stack

```
[ Samsung S21 / Browser ]
           │
     (PWA / HTTPS)
           │
           ▼
┌────────────────────────────────────────┐
│             FastAPI Backend            │
│  ├── Shift Scheduler (3-3-3 Math)      │
│  ├── Smart URL Scraper (BeautifulSoup) │
│  ├── IMAP Email Radar (Domain Match)   │
│  └── WebPush Dispatcher (VAPID)        │
└────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│            SQLite Database             │
│  ├── applications (Jobs / Grants)      │
│  ├── tasks (Streaks / University)      │
│  └── push_subscriptions (Devices)      │
└────────────────────────────────────────┘
```

* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **Database:** SQLite3
* **Scraping:** BeautifulSoup4, HTTPX
* **Frontend:** HTML5, CSS3 (Cyberpunk/Dark Mode), Vanilla JavaScript, Service Workers
* **Security:** VAPID Elliptic Curve Push Encryption, IMAP SSL

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hardex001-tech/chronos.git
   cd chronos
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your shift start date and preferences.

4. **Launch Chronos:**
   ```bash
   python run.py
   ```
   Access the dashboard at `http://localhost:8000`.

---

## 📱 Mobile Installation (Samsung Galaxy / Android)
1. Ensure your phone is connected to the same Wi-Fi network as your PC (or access your deployed cloud URL).
2. Open `http://<your-pc-ip>:8000` in Google Chrome on your Samsung phone.
3. Tap the Chrome menu (⋮) and tap **"Install App"** (or *Add to Home screen*).
4. Chronos will install directly onto your home screen with a native full-screen app icon!

---

## 👤 Author
* **Abdulrazaq Adeyemi** — [@hardex001-tech](https://github.com/hardex001-tech)  
* Undergraduate Cybersecurity Student @ Federal University of Agriculture, Abeokuta (FUNAAB)
