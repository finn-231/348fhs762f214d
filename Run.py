from Receiver_Microservice.API.app import ReceiverListener
from Light_Microservice.API.app import LightListener
from Cleaning_Microservice.API.app import CleaningListener
from BMS.app import BMSListener
from Gateway.app import GatewayListener
import threading
import requests
from Credentials import storecreds as cfg
import time

# Receiver will handle messages and write them to the database
#rc = Receiver()
#thread_receiver = threading.Thread(target=rc.start_rabbitmq_consumer)
#thread_receiver.start()

# the calculator is pulling data from the database and doing calculations on it
#calc = Calculator()
# cleaning thread
#thread_cleaning = threading.Thread(target=calc._fetch_data_loop_cleaning)
# thread_cleaning.start()
# light thread
#thread_light = threading.Thread(target=calc._fetch_data_loop_light)
# thread_light.start()

# BMS Listener
#bms = BMSListener()
#thread_bms = threading.Thread(target=bms.start_listening)
# thread_bms.start()

# Gateway
#gw = GatewayListener()
#thread_gw = threading.Thread(target=gw.start_listening)
#thread_gw.start()

def start_apis():
    # Receiver
    rl = ReceiverListener()
    thread_receiver = threading.Thread(target=rl.start_listening)
    thread_receiver.start()
    # Light Microservice
    ll = LightListener()
    thread_light = threading.Thread(target=ll.start_listening)
    thread_light.start()
    # Cleaning Microservice
    cl = CleaningListener()
    thread_cleaning = threading.Thread(target=cl.start_listening)
    thread_cleaning.start()

    # Gateway
    gw = GatewayListener()
    thread_gw = threading.Thread(target=gw.start_listening)
    thread_gw.start()

def start_receiver():
    requests.post(f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/start")

def start_light():
    requests.post(f"http://{cfg.httprequests['light_ms']}:{cfg.httprequests['light_port']}/start")

def start_cleaning():
    requests.post(f"http://{cfg.httprequests['cleaning_ms']}:{cfg.httprequests['cleaning_port']}/start")

thread_apis = threading.Thread(target=start_apis)
thread_apis.start()

time.sleep(5)

thread_receiver = threading.Thread(target=start_receiver)
thread_receiver.start()
thread_light = threading.Thread(target=start_light)
thread_light.start()
thread_cleaning = threading.Thread(target=start_cleaning)
thread_cleaning.start()
# response2 = requests.post('http://127.0.0.1:5004/start')
# requests.post('http://127.0.0.1:5004/start')
# response = requests.post('http://127.0.0.1:5003/getdata')