from Input.Receiver.Receiver import Receiver
from Output.Calculator.Calculator import Calculator
import threading

rc = Receiver()
thread_receiver = threading.Thread(target=rc.start_rabbitmq_consumer)
thread_receiver.start()


calc = Calculator()
thread_cleaning = threading.Thread(target=calc._fetch_data_loop_cleaning)
thread_cleaning.start()

thread_light = threading.Thread(target=calc._fetch_data_loop_light)
thread_light.start()

