# Imagen base con Python
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de la app
RUN mkdir /app
RUN mkdir /app/shared
WORKDIR /app

# Copiar los archivos del servidor y dependencias
COPY files/server.py /app/server.py
COPY files/requirements.txt /app/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 65432

# Comando de inicio
CMD ["python", "server.py"]
