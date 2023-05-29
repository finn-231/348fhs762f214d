#!/usr/bin/env python
sql_database = {
    "host": "127.0.0.1",
    "user": "root",
    "passwd": "2103w9II",
    "db": "northwind",
}
rabbitmq = {
    "host": "localhost",
    "queue": "answer"
}
mongo_database = {
    "myclient": "mongodb+srv://finn_waehlt:dBXyAdWQf4t44ShXW1@cluster0.z2cr85t.mongodb.net/test",
    "mydb": "dev3",
    "mycol": "tickets"
}
httprequests = {
    "bms": "127.0.0.1", # add more if neccessary
    "bms_port": 5000,

    "gateway": "127.0.0.1",
    "gateway_port": 5001,

    # Microservice APIs
    "cleaning_ms": "127.0.0.1",
    "cleaning_port": 5002,

    "light_ms": "127.0.0.1",
    "light_port": 5003,

    "receiver_ms": "127.0.0.1",
    "receiver_port": 5004

}
config = {
    "ticket_time": 20 # put in the time when to check the tickets in a 24 hr format
}