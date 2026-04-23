from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import admin, motorizado, cliente

# 1. CREACIÓN DE TABLAS
# Al arrancar, FastAPI revisa models.py y crea el archivo .db si no existe.
models.Base.metadata.create_all(bind=engine)

# 2. INSTANCIA DE LA APP
app = FastAPI(
    title="Gestión de Entregas Oscar",
    description="Sistema MVP para control de pedidos y logística",
    version="1.0.0"
)

# --- NUEVO BLOQUE CORS ---
# Esto permite que tus archivos HTML hablen con tu servidor Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción se pone el dominio real, por ahora permitimos todo
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, PUT, DELETE
    allow_headers=["*"],
)
# -------------------------

# 3. CONEXIÓN DE DEPARTAMENTOS (Routers)
# Aquí pegamos los archivos de la carpeta /routers al servidor principal.
app.include_router(admin.router, prefix="/admin", tags=["Administrador"])
app.include_router(motorizado.router, prefix="/motorizado", tags=["Motorizado"])
app.include_router(cliente.router, prefix="/cliente", tags=["Cliente"])

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# 4. RUTA DE BIENVENIDA
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/cliente.html", "r", encoding="utf-8") as f:
        return f.read()
"""
@app.get("/")
async def inicio():
    return {
        "mensaje": "Servidor de Entregas Oscar - Activo",
        "documentacion": "/docs",
        "estado": "Funcionando"
    }
"""