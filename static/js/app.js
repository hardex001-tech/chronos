// Chronos Frontend Engine

document.addEventListener("DOMContentLoaded", () => {
  initApp();
  registerServiceWorker();
});

async function initApp() {
  await loadShiftStatus();
  try { await fetch("/api/tasks/sync"); } catch(e) {}
  await loadTasks();
  await loadApplications();
  setupEventListeners();
}

// 1. Shift Status & 24h Routine
async function loadShiftStatus() {
  try {
    const res = await fetch("/api/shift/status");
    const data = await res.json();

    document.getElementById("shift-title").textContent = data.shift_title;
    document.getElementById("shift-date").textContent = `${data.target_date_human} • Cycle Day ${data.cycle_day_index}/9`;
    
    const pill = document.getElementById("shift-pill");
    pill.textContent = data.shift_type.toUpperCase();
    pill.style.background = `${data.badge_color}22`;
    pill.style.color = data.badge_color;
    pill.style.border = `1px solid ${data.badge_color}55`;

    document.getElementById("energy-text").innerHTML = `<strong>Energy Profile (${data.energy_level}):</strong> ${data.energy_desc}`;
    document.getElementById("next-phase-text").textContent = `Next Transition: ${data.next_phase}`;

    // Render 24h Timeline
    const timelineList = document.getElementById("timeline-list");
    timelineList.innerHTML = "";
    data.daily_plan.forEach(item => {
      const el = document.createElement("div");
      el.className = "timeline-item";
      el.innerHTML = `
        <span class="timeline-time">${item.time}</span>
        <span class="timeline-activity">${item.activity}</span>
        <span class="timeline-category">${item.category}</span>
      `;
      timelineList.appendChild(el);
    });
  } catch (err) {
    console.error("Failed to load shift status", err);
  }
}

// 2. Daily Streaks & Tasks
async function loadTasks() {
  try {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();
    const list = document.getElementById("task-list");
    list.innerHTML = "";

    tasks.forEach(t => {
      const card = document.createElement("div");
      card.className = `task-card ${t.completed_today ? "completed" : ""}`;
      card.innerHTML = `
        <div class="task-left">
          <div class="task-checkbox ${t.completed_today ? "checked" : ""}" onclick="toggleTask(${t.id})">
            ${t.completed_today ? "✓" : ""}
          </div>
          <div class="task-info">
            <h4>${t.title}</h4>
            <p>${t.category} ${t.target_link ? `• <a href="${t.target_link}" target="_blank" style="color: #00E5FF; text-decoration:none;">Open Lab ↗</a>` : ""}</p>
          </div>
        </div>
        <div class="streak-pill">
          🔥 ${t.streak_count}d
        </div>
      `;
      list.appendChild(card);
    });
  } catch (err) {
    console.error("Failed to load tasks", err);
  }
}

async function toggleTask(taskId) {
  try {
    await fetch(`/api/tasks/${taskId}/toggle`, { method: "POST" });
    await loadTasks();
  } catch (err) {
    console.error("Failed to toggle task", err);
  }
}

// 3. Applications & Tracked Opportunities
async function loadApplications() {
  try {
    const res = await fetch("/api/apps");
    const apps = await res.json();
    const grid = document.getElementById("apps-grid");
    grid.innerHTML = "";

    apps.forEach(app => {
      const card = document.createElement("div");
      card.className = "app-card";
      
      const logoSrc = app.logo_url || "https://www.google.com/s2/favicons?domain=example.com&sz=64";
      const statusClass = app.status.includes("Review") ? "status-Review" :
                          app.status.includes("Ongoing") ? "status-Ongoing" :
                          app.status.includes("Progress") ? "status-Progress" : "status-Applied";

      card.innerHTML = `
        <div>
          <div class="app-header">
            <img class="app-logo" src="${logoSrc}" alt="${app.company}" onerror="this.src='https://www.google.com/s2/favicons?domain=google.com&sz=64'">
            <div class="app-title-box">
              <h4>${app.title}</h4>
              <p>${app.company} • ${app.category}</p>
            </div>
          </div>
          ${app.notes ? `<div class="app-notes" style="margin-top: 10px;">${app.notes}</div>` : ""}
        </div>
        <div class="app-footer">
          <span class="status-badge ${statusClass}">${app.status}</span>
          <a class="app-link-btn" href="${app.url}" target="_blank">Launch Portal ↗</a>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    console.error("Failed to load applications", err);
  }
}

// 4. Modal & URL Auto-Scraping
function setupEventListeners() {
  const modal = document.getElementById("modal-overlay");
  const openBtn = document.getElementById("open-modal-btn");
  const closeBtn = document.getElementById("close-modal-btn");
  const urlInput = document.getElementById("app-url-input");

  openBtn.addEventListener("click", () => modal.classList.add("active"));
  closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });

  // Real-time URL Metadata Scraper
  let debounceTimeout = null;
  urlInput.addEventListener("input", () => {
    clearTimeout(debounceTimeout);
    const url = urlInput.value.trim();
    if (url.length > 8 && (url.startsWith("http://") || url.startsWith("https://"))) {
      debounceTimeout = setTimeout(() => triggerScrape(url), 600);
    }
  });

  // Submit Application Form
  const form = document.getElementById("app-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      title: document.getElementById("app-title-input").value,
      company: document.getElementById("app-company-input").value,
      url: document.getElementById("app-url-input").value,
      category: document.getElementById("app-category-select").value,
      status: document.getElementById("app-status-select").value,
      notes: document.getElementById("app-notes-input").value,
      logo_url: document.getElementById("app-logo-input").value,
      sender_domain: document.getElementById("app-domain-input").value
    };

    try {
      await fetch("/api/apps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      modal.classList.remove("active");
      form.reset();
      document.getElementById("scrape-preview").classList.remove("active");
      await loadApplications();
    } catch (err) {
      alert("Error saving application");
    }
  });
}

async function triggerScrape(url) {
  const preview = document.getElementById("scrape-preview");
  preview.innerHTML = "<span style='font-size:12px; color:#94A3B8;'>⚡ Chronos is scraping metadata...</span>";
  preview.classList.add("active");

  try {
    const res = await fetch("/api/apps/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const meta = await res.json();

    document.getElementById("app-title-input").value = meta.title || meta.company;
    document.getElementById("app-company-input").value = meta.company;
    document.getElementById("app-domain-input").value = meta.sender_domain;
    document.getElementById("app-logo-input").value = meta.logo_url;

    preview.innerHTML = `
      <img src="${meta.logo_url}" style="width:24px; height:24px; border-radius:4px; background:#fff; padding:2px;">
      <div style="font-size:12px;">
        <strong>${meta.company}</strong> — ${meta.title.substring(0, 45)}...
      </div>
    `;
  } catch (err) {
    preview.innerHTML = "<span style='font-size:12px; color:#94A3B8;'>Auto-detected URL domain. Fill title manually.</span>";
  }
}

// 5. Service Worker & Push Notifications
function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js")
      .then(reg => {
        console.log("Chronos Service Worker registered on device", reg);
      })
      .catch(err => {
        console.warn("Service worker registration failed", err);
      });
  }
}

// Request Push Notification Permission
async function requestPushPermission() {
  if (!("Notification" in window)) {
    alert("This browser does not support notifications.");
    return;
  }
  const perm = await Notification.requestPermission();
  if (perm === "granted") {
    alert("✅ Push notifications enabled on your device!");
    // Trigger test push
    await fetch("/api/push/test", { method: "POST" });
  } else {
    alert("Notification permission denied or dismissed.");
  }
}
