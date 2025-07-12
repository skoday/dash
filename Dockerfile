FROM python:3.12.9-bullseye

WORKDIR /dash

# Copiar solo los archivos necesarios para instalar dependencias
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (Dash normalmente usa 8050)
EXPOSE 80

# Comando para correr la app
CMD ["python", "dashboard/app.py"]