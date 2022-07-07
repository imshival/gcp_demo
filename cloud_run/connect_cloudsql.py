import mysql.connector
import pandas as pd
from datetime import datetime
from gcloud import storage


client = storage.Client()


def get_current_date():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print("date and time =", dt_string)


def connect_sql():
    cnx = mysql.connector.connect(user='root', password='part1-sql-storage', host='34.133.14.181', database='covid22')
    # mycursor = cnx.cursor()
    # mycursor.execute("SELECT * FROM Persons")
    # myresult = mycursor.fetchall()
    city = 'patna'
    query = f"SELECT * FROM Persons WHERE city ='{city}'"

    df = pd.read_sql(query, cnx)
    print('hello')
    df['last_update'] = pd.to_datetime('now',utc=True).strftime("%m/%d/%Y")
    print(df)
    df.to_csv('out.csv')
    bucket = client.get_bucket('ad_data_raw')
    blob = bucket.blob('api/api_cloud_sql.csv')
    blob.upload_from_filename('out.csv')
    # print(df)
    # for x in myresult:
    #     print(x)
    cnx.close()
    return df




connect_sql()
