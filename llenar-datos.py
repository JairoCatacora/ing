import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def cargar_a_dynamodb(archivo_json, nombre_tabla):
    """
    Carga objetos JSON de un archivo a una tabla DynamoDB.

    :param archivo_json: Ruta al archivo JSON que contiene una lista de objetos.
    :param nombre_tabla: Nombre de la tabla DynamoDB.
    """
    try:
        # Leer el archivo JSON
        with open(archivo_json, 'r') as archivo:
            datos = json.load(archivo)
        
        # Validar que el archivo contiene una lista
        if not isinstance(datos, list):
            raise ValueError("El archivo JSON debe contener una lista de objetos.")
        
        # Inicializar el cliente DynamoDB
        dynamodb = boto3.resource('dynamodb')
        tabla = dynamodb.Table(nombre_tabla)
        
        # Agregar cada objeto a la tabla
        for item in datos:
            tabla.put_item(Item=item)
            print(f"Objeto agregado: {item}")
        
        print("Carga completada con éxito.")
    
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_json}' no existe.")
    except json.JSONDecodeError:
        print("Error: El archivo no tiene un formato JSON válido.")
    except (BotoCoreError, ClientError) as error:
        print(f"Error al interactuar con DynamoDB: {error}")
    except Exception as e:
        print(f"Se produjo un error: {e}")
