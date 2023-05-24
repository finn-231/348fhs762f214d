from Input.Receiver.Receiver import Receiver
from Output.Calculator.Calculator import Calculator
from BMS.app import BMSListener
import threading

# Receiver will handle messages and write them to the database
rc = Receiver()
thread_receiver = threading.Thread(target=rc.start_rabbitmq_consumer)
thread_receiver.start()

# the calculator is pulling data from the database and doing calculations on it
calc = Calculator()
# cleaning thread
thread_cleaning = threading.Thread(target=calc._fetch_data_loop_cleaning)
thread_cleaning.start()
# light thread
thread_light = threading.Thread(target=calc._fetch_data_loop_light)
thread_light.start()

# BMS Listener
bms = BMSListener()
thread_bms = threading.Thread(target=bms.start_listening)
thread_bms.start()