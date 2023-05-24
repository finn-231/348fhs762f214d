import time
from Modules.DataReader.DataReader import DataReader
from Modules.DataWriterMongo.DataWriterMongo import DataWriterMongo
from Modules.TicketCreator.Ticket import Ticket
from Credentials import storecreds as cfg
from Modules.HTTPrequester.HTTPrequester import HTTPrequester


class Calculator:
    def __init__(self):
        self.database = None
        self.is_running = True

    def stop(self):
        self.is_running = False

    def _fetch_data_loop_cleaning(self):
        import time
        import datetime

        dr = DataReader()
        dr.connect()
        # get all rooms as an array
        room_array = dr.get_single_field(table_name="Room", field="ID")
        rooms = []
        for row in room_array:
            for room in row:
                rooms.append(room)

        while self.is_running:
            current_time = datetime.datetime.now().time()
            target_time = datetime.time(cfg.config["ticket_time"], 0)  # 20:00

            # self.check_for_ticket() # just for testing

            if current_time >= target_time:
                self.check_for_ticket(rooms=rooms)
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
        dr = DataReader()
        dr.connect()
        # get all rooms as an array
        room_array = dr.get_single_field(table_name="Room", field="ID")
        rooms = []
        for row in room_array:
            for room in row:
                rooms.append(room)

        prev_occ = {}
        while self.is_running:
            # Perform custom operations on the data
            self.check_for_light(rooms, prev_occ=prev_occ)
            # Sleep for 5 seconds
            time.sleep(2)

    def check_for_ticket(self, rooms):
        # check if total people entering per room has passed 20
        dr = DataReader()
        dr.connect()
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
                # ticket needs to be sent
                # create ticket
                print(
                    f"#[Calculator]: Occupancy for room {room} surpassed the limit. Creating ticket...\n"
                )
                ticket = Ticket(room=room, occupancy=count)
                dataToWrite = ticket.getTicketAsCollection()
                mongowriter = DataWriterMongo()
                mongowriter.insert_ticket(dataToWrite)
            else:
                print(
                    f"#[Calculator]: Occupancy for room {room} is below the limit. Passing room...\n"
                )

    def check_for_light(self, rooms, prev_occ):
        dr = DataReader()
        dr.connect()
        # lets create key_value pairs to make a object we can reference to
        for room in rooms:
            # get the current occupancy
            query = f"SELECT (SELECT COUNT(*) FROM data d INNER JOIN Sensor s ON d.sensor_id = s.ID WHERE s.room_id = '{room}' AND d.direction = 'in' AND DATE(d.timestamp) = CURDATE()) AS in_count, (SELECT COUNT(*) FROM data d INNER JOIN Sensor s ON d.sensor_id = s.ID WHERE s.room_id = '{room}' AND d.direction = 'out' AND DATE(d.timestamp) = CURDATE()) AS out_count;"
            result = dr.custom_query(query)

            in_count, out_count = result[0]
            total_count = in_count - out_count
            
            # check if we are in the first cycle or the room even exists to take into the array
            if prev_occ.get(room) == None:
                prev_occ[room] = total_count
            else:
                # check if this count is larger than zero and larger than the old count and make sure the old one is smaller than one
                # if yes, send request to turn on the light
                if total_count > 0 and total_count > prev_occ.get(room) and prev_occ.get(room) <= 0:
                    print(f"#[Calculator]: Turning on light in room {room}...\n")
                    
                    # get all the light_ids for this room
                    query = f"SELECT ID FROM Light WHERE room_id = '{room}'"
                    light_result = dr.custom_query(query)
                    light_ids = []
                    for row in light_result:
                        for id in row:
                            light_ids.append(id)

                    payload = {
                        "switch":1,
                        "lights":light_ids
                    }

                    http_requester = HTTPrequester(receiver="bms", port="bms_port")  # Replace with the desired IP address
                    # Make the HTTP request
                    try:
                        http_requester.make_request('lights', payload)
                    except ConnectionRefusedError:
                        print(f"#[Calculator]: Can't turn on light in room {room}. Error: Connection Refused.\n")
                    except Exception as e:
                        print(f"#[Calculator]: Can't turn on light in room {room}. Error: {e}\n")
                # check if the count is smaller than zero and smaller than the last one
                elif total_count <= 0 and total_count < prev_occ.get(room):
                    print(f"#[Calculator]: Turning off light in room {room}...\n")

                    # get all the light_ids for this room
                    query = f"SELECT ID FROM Light WHERE room_id = '{room}'"
                    light_result = dr.custom_query(query)
                    light_ids = []
                    for row in light_result:
                        for id in row:
                            light_ids.append(id)

                    
                    payload = {
                        "switch":0,
                        "lights":light_ids
                    }

                    http_requester = HTTPrequester(receiver="bms", port="bms_port")  # Replace with the desired IP address
                    # Make the HTTP request
                    try:
                        http_requester.make_request('lights', payload)
                    except ConnectionRefusedError:
                        print(f"#[Calculator]: Can't turn off light in room {room}. Error: Connection Refused.\n")
                    except Exception as e:
                        print(f"#[Calculator]: Can't turn off light in room {room}. Error: {e}\n")

            # assign current values to prev_occ
            prev_occ[room] = total_count