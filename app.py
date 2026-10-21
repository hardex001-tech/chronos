from a2wsgi import ASGIMiddleware
from run import app as asgi_app

# WSGI adapter: ensures default Azure Gunicorn runner runs FastAPI ASGI seamlessly with zero 500 error!
app = ASGIMiddleware(asgi_app)

if __name__ == "__main__":
    import uvicorn
    from config.settings import settings
    uvicorn.run("run:app", host=settings.HOST, port=settings.PORT, reload=True)
