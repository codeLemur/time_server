import logging
from flask import Flask, request

import data_handler
import globals
import state_machine

app = Flask(__name__)
dh = data_handler.DataHandler()
sm = state_machine.StateMachine()


@app.route('/', methods=['GET', 'POST'])
def index():
    result = -1
    if request.method == 'POST':
        data = request.get_json()
        logging.info(f'Received POST request with data: {data}')
        if data[globals.COMMAND_TYPE_KEY] == globals.CMD_STATE_CHANGE:
            handle_state_change_command(data)
            result = 0
        elif data[globals.COMMAND_TYPE_KEY] == globals.CMD_REPORT_TIME:
            handle_report_time_command(data)
            result = 0
        else:
            logging.error(f'Received invalid command: {data[globals.COMMAND_TYPE_KEY]}')

        return result  # 0 for success, -1 for error
    elif request.method == 'GET':
        logging.info('Received GET request, return current State')  # TODO remove to speed this up
        return sm.get_current_state().value
    else:
        return 'Hello, world!'


@app.route('/')
def hello():
    return 'Hello, world!'


def handle_state_change_command(data: dict):
    if sm.update(data[globals.EVENT_KEY]):
        # State changed do entry action for specific states
        if sm.get_current_state() == globals.States.STOPPED:
            dh.calculate_race_duration()


def handle_report_time_command(data: dict):
    dh.save_timestamp(data)
    if globals.ROLE_KEY in data:
        if data[globals.ROLE_START]:
            dh.set_last_start_time(data)
        elif data[globals.ROLE_GOAL]:
            dh.set_last_goal_time(data)
            dh.calculate_race_duration()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Start Server')
    app.run(debug=True, host='0.0.0.0', port=80)

