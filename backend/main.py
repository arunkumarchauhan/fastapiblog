from fastapi import FastAPI
from core.config import settings
from db.session import engine, Base

def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    create_tables()
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)

    return app

app=start_application()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API!"}