import csv
import globals
import logging
import os
import time


class DataHandler:
    DATA_PATH = 'data'
    TIMESTAMPS_FILENAME = os.path.join(DATA_PATH, 'timestamps.csv')

    def __init__(self):
        if not os.path.exists(self.DATA_PATH):
            os.makedirs(self.DATA_PATH)
        with open(self.TIMESTAMPS_FILENAME, 'w', newline='') as timestamp_file:
            self.fieldnames = [globals.ROLE_KEY, globals.START_NUMBER_KEY, globals.TIMESTAMP_KEY]
            writer = csv.DictWriter(timestamp_file, fieldnames=self.fieldnames)
            writer.writeheader()

    def save_timestamp(self, timestamp_data: dict) -> None:
        with open(self.TIMESTAMPS_FILENAME, 'a', newline='') as timestamp_file:
            writer = csv.DictWriter(timestamp_file, fieldnames=self.fieldnames)
            writer.writerow(timestamp_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('PyCharm')

    dh = DataHandler()
    while True:
        dh.save_timestamp({globals.ROLE_KEY: globals.ROLE_START, globals.START_NUMBER_KEY: 1, globals.TIMESTAMP_KEY: round(time.time(), 2)})
        input("Press enter to store next time stamp")
