"""This file will handle the requests to the Database Interfacer Service."""
"""Needs to be implemented correctly -- using a mock for now."""

class DBInterfacer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, data):
        print("Data was inserted to the database: {0}".format(data))
