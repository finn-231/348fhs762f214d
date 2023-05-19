import mysql.connector
import json

class DataWriter:
    def __init__(self):
        self.connection = None

    def connect(self):
        # Replace the connection parameters with your specific MySQL database details
        db_host = '127.0.0.1'
        db_user = 'root'
        db_password = '2103w9II'
        db_name = 'northwind'

        # Establish the database connection
        self.connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP,
            sensor_id VARCHAR(255),
            room_id VARCHAR(255),
            direction VARCHAR(255),
            FOREIGN KEY (room_id) REFERENCES Room(ID),
            FOREIGN KEY (sensor_id) REFERENCES Sensor(ID)
        )
        '''
        self.connection.cursor().execute(query)
        self.connection.commit()

    def insert_data(self, sensor_id, room_id, direction, timestamp):
        query = '''
        INSERT INTO data (timestamp, sensor_id, room_id, direction) VALUES (%s, %s, %s, %s)
        '''
        values = (timestamp, sensor_id, room_id, direction)
        self.connection.cursor().execute(query, values)
        self.connection.commit()

    def write_data(self, data):
            sensor_id = data.get('unit_id')
            room_id = data.get('room')
            direction = data.get('direction')
            timestamp = data.get('timestamp')
            self.insert_data(sensor_id=sensor_id, room_id=room_id, direction=direction, timestamp=timestamp)

    def write_json_data(self, json_str):
        parsed_data = json.loads(json_str)
        self.connect()
        # self.create_table()
        self.write_data(parsed_data)
        self.disconnect()
