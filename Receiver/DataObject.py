# DataObject to hold the data and timestamp
import time

class DataObject:
    def __init__(self):
        self.timestamp = time.time()
        self.data = []

    def add_data(self, data):
        self.data.append(data)