
import pymysql 

#function to establish connection to the database
def read_data_from_database (): 
    connection = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'your_password',
        database = 'your_database'
    )
    
    #created a cursor object to execute SQL queries on the database
    cursor = connection.cursor()

    #customize the query 
    query = "SELECT * FROM rooms"
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
# data = read_data_from_database("rooms")
print(data)
