from run import app

if __name__ == "__main__":
    import uvicorn
    from config.settings import settings
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)
