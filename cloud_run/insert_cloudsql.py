import mysql.connector


def insert_sql(patient_id, last_name, first_name, address, city):
    cnx = mysql.connector.connect(user='root', password='part1-sql-storage', host='34.133.14.181', database='covid22')
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
