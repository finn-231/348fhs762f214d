import requests
from Credentials import storecreds as cfg

class HTTPrequester:
    def __init__(self, receiver):
        self.ip_address = cfg.httprequests[receiver]

    def make_request(self, endpoint, payload):
        url = f'http://{self.ip_address}/{endpoint}'
        response = requests.post(url, data=payload)

        if response.status_code == requests.codes.ok:
            print('Request sent successfully.')
        else:
            print('An error occurred while sending the request.')

