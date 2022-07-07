import mysql.connector
import pandas as pd
from datetime import datetime
from gcloud import storage


client = storage.Client()


def send_api_data_to_gcs():
    cnx = mysql.connector.connect(user='root', password='part1-sql-storage', host='34.133.14.181', database='covid22')
    city = 'patna'
    query = f"SELECT * FROM Persons WHERE city ='{city}'"
    df = pd.read_sql(query, cnx)
    # print('hello')
    df['last_update'] = pd.to_datetime('now', utc=True).strftime("%m/%d/%Y")
    # print(df)
    # df.to_csv('out.csv')
    bucket = client.get_bucket('ad_data_raw')
    bucket.blob('api/test.csv').upload_from_string(df.to_csv(), 'text/csv')
    cnx.close()
    return "file uploaded to GCS Bucket"

send_api_data_to_gcs()