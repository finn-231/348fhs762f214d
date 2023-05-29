from flask import Flask, jsonify, request
from Credentials import storecreds as cfg
from Cleaning_Microservice.Cleaning import Cleaning

class CleaningListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["cleaning_ms"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["cleaning_port"]
        self.ms = Cleaning()

        @self.app.route('/start', methods=['POST'])
        def start_ms():
            self.ms._fetch_data_loop_cleaning()
            print("#[Cleaning_API]: Microservices started")
            return 'OK'
        
        @self.app.route('/gettickets', methods=['POST'])
        def get_data():
            data = self.ms.get_tickets()
            return jsonify(data)


    def start_listening(self):
        print(f"#[Cleaning_MS]: Listening on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

