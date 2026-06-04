from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import router

app = FastAPI(title="Smart Task Planner", description="Планировщик задач с AI-заглушкой и веб-интерфейсом")

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "message": "Сервер работает"}