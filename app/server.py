# app/server.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()

# 1. Servimos la app web de Flet (compilada)
app.mount("/app", StaticFiles(directory="build/web", html=True), name="app")

# 2. Servimos la landing page (index.html)
@app.get("/")
def home():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
