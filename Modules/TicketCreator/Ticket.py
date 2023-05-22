from datetime import datetime
import time
import json

class Ticket:

    def __init__(self, room):
        self.room = room
        dt = datetime.now()
        new_dt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-2]
        print(new_dt) # das print war nur zum testen, das braucht man eig. nicht

    def convertRoomInJSON(self, roomID):
        json_string = json.dumps(roomID)
        return json_string
    
    def convertTSInJSON(self, ts):
        json_string = json.dumps(ts)
        return json_string









       # raumnummer
       # id
       # timestamp (automatisch zu dem zeitpunkt als ticket kreiert wurde)

       # methode die objekte in jSON format umschreibt (objekte sind raumnummer und timestamp)
       
