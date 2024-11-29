# Imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY main.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Variables de entorno
ENV AWS_REGION=us-east-1
ENV DYNAMO_TABLE=TablaWebScrapping-IGP
ENV S3_BUCKET=pf-bucket-ingest
ENV OUTPUT_FILENAME=data.csv

# Comando por defecto para ejecutar el script
CMD ["python", "main.py"]
