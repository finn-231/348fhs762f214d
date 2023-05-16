# DataObject to hold the data and timestamp
import time

class DataObject:
    def __init__(self):
        self.data = []
        self.timestamp = time.time()

    def add_data(self, received_data):
        self.data.append(received_data)