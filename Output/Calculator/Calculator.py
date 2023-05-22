import time
from Modules.DataReader.DataReader import DataReader
from Modules.DataWriterMongo.DataWriterMongo import DataWriterMongo


class Calculator:
    def __init__(self):
        self.database = None
        self.is_running = True

    def stop(self):
        self.is_running = False

    def _fetch_data_loop_cleaning(self):

        import time
        import datetime

        while self.is_running:
        
            current_time = datetime.datetime.now().time()
            target_time = datetime.time(20, 0)  # 20:00

            if current_time >= target_time:
                self.check_for_ticket()
                # Sleep for 24 hours before checking again
                time.sleep(24 * 60 * 60)
            else:
                # Calculate the time remaining until 20:00
                time_remaining = (
                    datetime.datetime.combine(datetime.date.today(), target_time)
                    - datetime.datetime.now()
                )
                # Sleep until 20:00
                time.sleep(time_remaining.total_seconds())


    def _fetch_data_loop_light(self):
        while self.is_running:
            # Perform custom operations on the data
            self.check_for_ticket()
            # Sleep for 5 seconds
            time.sleep(5)

    def check_for_ticket(self):
        # check if total people entering per room has passed 20
        dr = DataReader()
        dr.connect()
        # get all rooms as an array
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
            if count > 20:
                print(f"limit surpassed ({count})")
                # ticket needs to be sent
                mongowriter = DataWriterMongo()
                data = [{"timestamp": "testtime", "room": room}]
                mongowriter.insert_ticket(data)
            else:
                print(f"limit not surpassed ({count})")
            # possibly send ticket
