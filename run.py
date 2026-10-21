import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from config.settings import settings
from database.db import init_db
from api.routes_shifts import router as shifts_router
from api.routes_apps import router as apps_router
from api.routes_tasks import router as tasks_router
from api.routes_push import router as push_router

# 1. Initialize SQLite Database
init_db()

# 2. FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="Shift-Adaptive Career & Cybersecurity Sentinel",
    version="1.0.0"
)

# 3. Mount Static Directory
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 4. Include API Routers
app.include_router(shifts_router)
app.include_router(apps_router)
app.include_router(tasks_router)
app.include_router(push_router)

# 5. Serve Single-Page App (SPA) Dashboard
@app.get("/")
def read_root():
    return FileResponse(str(BASE_DIR / "templates" / "index.html"))

if __name__ == "__main__":
    print(f"==================================================")
    print(f" ⚡ {settings.APP_NAME} Sentinel is launching...")
    print(f" • Host: http://localhost:{settings.PORT}")
    print(f" • Local Network (for Samsung S21): http://<Your-PC-IP>:{settings.PORT}")
    print(f" • User: {settings.USER_NAME}")
    print(f" • Rotation Anchor: {settings.SHIFT_ANCHOR_DATE} (Morning Day 1)")
    print(f"==================================================")
    uvicorn.run("run:app", host=settings.HOST, port=settings.PORT, reload=True)
