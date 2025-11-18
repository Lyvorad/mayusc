# app/server.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import threading
import uvicorn
import os
from main import main as flet_main  # importamos la función main de flet

import flet as ft

app = FastAPI()

# Lanzar Flet en hilo separado
def start_flet():
    ft.app(target=flet_main, view=None, port=8550, assets_dir="static")

t = threading.Thread(target=start_flet, daemon=True)
t.start()

# Redirige la raíz del servicio app.mayusc.lat al puerto interno donde escucha Flet
@app.get("/")
async def root():
    # Si Flet expone una UI web, lo ideal es redirigir al cliente al puerto/endpoint
    # o servir un proxy. Render/Cloudflare enruta el tráfico HTTP a este servicio,
    # así que retornamos una redirección al mismo host en la ruta que necesites.
    # Si prefieres proxear, necesitarás configurar un proxy inverso; esto es una
    # redirección simple que funcionará si Flet sirve su UI accesible públicamente.
    return RedirectResponse(url="/flet")

# Ruta ejemplo para evitar 404
@app.get("/flet")
async def flet_ui_redirect():
    # Si tu Flet UI está "embebida" disponible en la raíz, aquí podrías retornar
    # contenido estático o redirigir al puerto interno. Muchas deploys usan un proxy.
    # Como solución simple, intentamos redirigir a una dirección que Cloud/Render
    # pueda enrutar internamente si está configurado.
    return {"message": "Flet app running (interno). Si ves esto, Flet arrancó correctamente."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
