
import pymysql 

#function to establish connection to the database
def read_data_from_database (): 
    connection = pymysql.connect(
        host = 'az-mysql-dbs-server.mysql.database.azure.com',
        user = 'sach',
        password = 'security@adm1n',
        database = 'room_data'
    )
    
    #created a cursor object to execute SQL queries on the database
    cursor = connection.cursor()

    #customize the query 
    query = "SELECT * FROM room"
    #query = f"SELECT * FROM {table_name}" 
    cursor.execute(query)
    rows = cursor.fetchall()

    # an empty list to store the retrieved data
    data = []
    for row in rows:
        data.append(row)

    cursor.close()
    connection.close()

    return data

from data_reader import read_data_from_database

data = read_data_from_database()
# data = read_data_from_database("room")
print(data)
