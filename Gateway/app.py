from flask import Flask, render_template, request
from Credentials import storecreds as cfg
import requests

class GatewayListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["gateway"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["gateway_port"]

        @self.app.route('/data', methods=['GET', 'POST'])
        def index():
            # get database stuff here

            query = 'SELECT * FROM data'
            response = requests.post(
                f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                data=query
            )
            data_result = response.json()
            print(data_result)
            # print(data_result)

            response = requests.post(
                f"http://{cfg.httprequests['cleaning_ms']}:{cfg.httprequests['cleaning_port']}/gettickets"
            )

            try:
                ticket_result = response.text
                print(ticket_result)
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to decode JSON response: {e}")
                print(f"Response content: {response.content}")
            
            
            return render_template('index.html', data=data_result, tickets=ticket_result)

        

    def start_listening(self):
        print(f"#[Gateway]: Waiting for connections on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

