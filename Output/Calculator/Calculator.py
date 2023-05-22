import time
from Modules.DataReader.DataReader import DataReader

class Calculator:
    def __init__(self):
        self.database = None
        self.is_running = True

    def stop(self):
        self.is_running = False

    def _fetch_data_loop_cleaning(self):
        dr = DataReader()
        dr.connect()
        while self.is_running:
            # Perform custom operations on the data
            self.check_for_ticket(dr)
            # Sleep for 5 seconds
            time.sleep(5)

    def _fetch_data_loop_light(self):
        dr = DataReader()
        dr.connect()
        while self.is_running:
            # Perform custom operations on the data
            self.check_for_ticket(dr)
            # Sleep for 5 seconds
            time.sleep(5)

    def check_for_ticket(self, dr):
        # check if total people entering per room has passed 20

        #get all rooms as an array
        room_array = dr.get_single_field(table_name="Room", field="ID")
        rooms = []
        for row in room_array:
            for room in row:
                rooms.append(room)

        # for each room
        for room in rooms:
            # build the query
            query = f"SELECT COUNT(*) AS total_rows FROM data d JOIN Sensor s ON d.sensor_id = s.ID JOIN Room r ON s.room_id = r.ID WHERE d.direction = 'in' AND r.ID = '{room}' AND DATE(d.timestamp) = CURDATE();;"
            # run the query
            count_array = dr.custom_query(query)
            for row in count_array:
                for count in row:
                    count = count
            # check if the value is over 20
            if count > 1:
                print(f"limit surpassed ({count})")
            else:
                print(f"limit not surpassed ({count})")
            # possibly send ticket
    