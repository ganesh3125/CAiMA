import sys
from AudioToText import AudioToTextConvertor
from DBase import DBConnection
import threading

class Runner:

    def __init__(self):
        connection = DBConnection.DBConnection()
        connection.connect()
        self.convertor = AudioToTextConvertor.AudioToTextConvertor(connection)

    def start_runner(self):
        self.convertor.count = 1
        x = threading.Thread(target=self.convertor.convert)
        x.start()

    def continue_runner(self):
        self.convertor.count = 1

    def stop_runner(self):
        self.convertor.count = 0

if __name__ == "__main__":
    runner = Runner()
    runner.start_runner()
