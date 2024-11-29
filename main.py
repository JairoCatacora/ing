import boto3
import csv
import os

# Configuración de AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMO_TABLE = os.getenv("DYNAMO_TABLE")
S3_BUCKET = os.getenv("S3_BUCKET")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "data.csv")

def fetch_dynamodb_data(table_name):
    """Obtiene todos los datos de una tabla DynamoDB manejando la paginación."""
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
    paginator = dynamodb.get_paginator("scan")
    response_iterator = paginator.paginate(TableName=table_name)

    items = []
    for page in response_iterator:
        items.extend(page.get("Items", []))
    
    return items

def write_csv(data, filename):
    """Escribe los datos obtenidos de DynamoDB en un archivo CSV."""
    if not data:
        print("No hay datos para escribir.")
        return
    
    # Normalizar datos para convertir de formato DynamoDB a dict
    normalized_data = [
        {k: list(v.values())[0] for k, v in item.items()} for item in data
    ]
    
    # Crear el archivo CSV
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=normalized_data[0].keys())
        writer.writeheader()
        writer.writerows(normalized_data)
    print(f"Archivo CSV generado: {filename}")

def upload_to_s3(filename, bucket_name):
    """Sube el archivo generado a un bucket S3."""
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        with open(filename, "rb") as file_data:
            s3.upload_fileobj(file_data, bucket_name, filename)
        print(f"Archivo {filename} subido exitosamente a S3 ({bucket_name})")
    except Exception as e:
        print(f"Error al subir archivo a S3: {e}")

def main():
    print("Iniciando proceso...")
    # Obtener datos de DynamoDB
    data = fetch_dynamodb_data(DYNAMO_TABLE)
    print(f"Registros obtenidos: {len(data)}")

    # Crear archivo CSV
    write_csv(data, OUTPUT_FILENAME)

    # Subir archivo a S3
    upload_to_s3(OUTPUT_FILENAME, S3_BUCKET)

if __name__ == "__main__":
    main()
