import mysql.connector

# Import the Secret Manager client library.
from google.cloud import secretmanager
import google_crc32c


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    # print("{}".format(payload))
    return payload



def insert_sql(patient_id, last_name, first_name, address, city):
    passwrd = access_secret_version("stone-lodge-353709","cloud-sql-password",1)
    cnx = mysql.connector.connect(user='root', password=passwrd, host='34.133.14.181', database='covid22')
    mycursor = cnx.cursor()
    # print("hello")
    # patient_id = 1119
    # last_name = "harish"
    # first_name = "kumar"
    # address = "boring_road"
    # city = "patna"
    if patient_id is not None or last_name is not None or first_name:
        print(patient_id, last_name, first_name, address, city)
        query = ("INSERT INTO Persons VALUES (%s ,%s,%s,%s,%s)")
        mycursor.execute(query, (patient_id, last_name, first_name, address, city))
        # Commit your changes in the database
        cnx.commit()
        cnx.close()
        return "success"
    else:
        return "failure"
