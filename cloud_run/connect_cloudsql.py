import mysql.connector

def connect_sql():
  cnx = mysql.connector.connect(user='root', password='part1-sql-storage', host='34.133.14.181', database='covid22')
  mycursor = cnx.cursor()
  mycursor.execute("SELECT * FROM Persons")
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)
  cnx.close()
  print(myresult)
  return myresult

