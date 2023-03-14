import logging
from flask import Flask, request

import datahandler
import globals

app = Flask(__name__)
dh = datahandler.DataHandler()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the data
        logging.info(f'Received POST request with data: {data}')
        dh.save_timestamp(data)
        if data[globals.ROLE_START]:
            dh.set_last_start_time(data)
        elif data[globals.ROLE_GOAL]:
            dh.set_last_goal_time(data)
            dh.calculate_race_duration()  # TODO move to other location, wait for confirmation if signal counts

        return 'Received POST request with data: {}'.format(data)
    else:
        return 'Hello, world!'


@app.route('/')
def hello():
    return 'Hello, world!'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Start Server')
    app.run(debug=True, host='0.0.0.0', port=80)

