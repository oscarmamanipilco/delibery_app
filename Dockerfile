FROM python:3.11-slim

WORKDIR /app

# Instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de tu carpeta actual al contenedor
COPY . .

# IMPORTANTE: Aquí llamamos a 'main:app' porque main.py está en la raíz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]