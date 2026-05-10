import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
import boto3

# Cargar .env
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")

S3_BUCKET = os.getenv("S3_BUCKET")

conexion = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

query = "SELECT * FROM alumnos"

df = pd.read_sql(query, conexion)

archivo_csv = "data.csv"

df.to_csv(archivo_csv, index=False)

print("CSV generado")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

s3.upload_file(archivo_csv, S3_BUCKET, archivo_csv)

print("Archivo subido a S3")

conexion.close()
