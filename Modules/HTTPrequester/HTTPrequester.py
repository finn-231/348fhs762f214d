import requests
from Credentials import storecreds as cfg

class HTTPrequester:
    def __init__(self, receiver, port):
        self.ip_address = cfg.httprequests[receiver]
        self.port = cfg.httprequests[port]

    def make_request(self, endpoint, payload):
        url = f'http://{self.ip_address}:{self.port}/{endpoint}'
        response = requests.post(url, data=payload)

        if response.status_code == requests.codes.ok:
            pass
        else:
            print(f"#[Calculator]: Request to {self.ip_address}:{self.port} failed. Make sure the instance is running.")

