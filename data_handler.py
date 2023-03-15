import csv
import globals
import logging
import os
import time
from datetime import datetime


class DataHandler:
    DATA_PATH = 'data'
    TIMESTAMPS_FILENAME = os.path.join(DATA_PATH, 'timestamps.csv')
    RACE_DATA_FILENAME = os.path.join(DATA_PATH, 'race_data.csv')

    def __init__(self):
        self.timestamp_fieldnames = [globals.ROLE_KEY, globals.START_NUMBER_KEY, globals.TIMESTAMP_KEY]
        self.race_data_fieldnames = [globals.START_NUMBER_KEY, globals.DURATION_KEY, globals.LOG_TIME_KEY]
        self._last_start_time = dict()
        self._last_goal_time = dict()

        if not os.path.exists(self.DATA_PATH):
            os.makedirs(self.DATA_PATH)
        if not os.path.exists(self.TIMESTAMPS_FILENAME):
            with open(self.TIMESTAMPS_FILENAME, 'w', newline='') as timestamp_file:
                writer = csv.DictWriter(timestamp_file, fieldnames=self.timestamp_fieldnames)
                writer.writeheader()
        if not os.path.exists(self.RACE_DATA_FILENAME):
            with open(self.RACE_DATA_FILENAME, 'w', newline='') as race_data_file:
                writer = csv.DictWriter(race_data_file, fieldnames=self.race_data_fieldnames)
                writer.writeheader()

    def set_last_start_time(self, timestamp_data: dict) -> None:
        self._last_start_time = timestamp_data

    def set_last_goal_time(self, timestamp_data: dict) -> None:
        self._last_goal_time = timestamp_data

    def save_timestamp(self, timestamp_data: dict) -> None:
        with open(self.TIMESTAMPS_FILENAME, 'a', newline='') as timestamp_file:
            writer = csv.DictWriter(timestamp_file, fieldnames=self.timestamp_fieldnames)
            writer.writerow(timestamp_data)

    def calculate_race_duration(self):
        start_time = self._last_start_time.get(globals.TIMESTAMP_KEY, 0)
        goal_time = self._last_goal_time.get(globals.TIMESTAMP_KEY, 0)
        duration_ms = goal_time - start_time
        start_number = self._last_start_time.get(globals.START_NUMBER_KEY)
        # Check that the duration_ms is not negative
        if duration_ms < 0:
            logging.error(f'Got negative duration : {duration_ms} ms')
        else:
            logging.info(f'Race duration for race number [{start_number}] is {duration_ms} ms')
            with open(self.RACE_DATA_FILENAME, 'a', newline='') as race_data_file:
                writer = csv.DictWriter(race_data_file, fieldnames=self.race_data_fieldnames)
                writer.writerow({globals.START_NUMBER_KEY: start_number,
                                 globals.DURATION_KEY: duration_ms,
                                 globals.LOG_TIME_KEY: datetime.fromtimestamp(goal_time // 1000)})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('PyCharm')

    dh = DataHandler()
    while True:
        dh.save_timestamp({globals.ROLE_KEY: globals.ROLE_SERVER, globals.START_NUMBER_KEY: 1, globals.TIMESTAMP_KEY: round(time.time(), 2)})
        input("Press enter to store next time stamp")
