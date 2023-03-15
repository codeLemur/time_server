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
    result = 'error'
    if request.method == 'POST':
        data = request.get_json()
        logging.info(f'Received POST request with data: {data}')
        if data[globals.COMMAND_TYPE_KEY] == globals.CMD_STATE_CHANGE:
            if handle_state_change_command(data):
                result = 'success'
        elif data[globals.COMMAND_TYPE_KEY] == globals.CMD_REPORT_TIME:
            if handle_report_time_command(data):
                result = 'success'
        else:
            logging.error(f'Received invalid command: {data[globals.COMMAND_TYPE_KEY]}')

        return result
    elif request.method == 'GET':
        logging.info('Received GET request, return current State')  # TODO remove to speed this up
        return sm.get_current_state().name
    else:
        return 'Hello, world!'


@app.route('/')
def hello():
    return 'Hello, world!'


def handle_state_change_command(data: dict) -> bool:
    result = False
    event = globals.Events[data[globals.EVENT_KEY]]
    # TODO check for roles?
    if sm.update(event):
        result = True
        # State changed do entry action for specific states
        if sm.get_current_state() == globals.States.STOPPED:
            dh.calculate_race_duration()

    return result


def handle_report_time_command(data: dict) -> bool:
    result = False
    data.pop(globals.COMMAND_TYPE_KEY)
    dh.save_timestamp(data)
    if globals.ROLE_KEY in data:
        if data[globals.ROLE_KEY] == globals.ROLE_START:
            if sm.get_current_state() == globals.States.READY:
                dh.set_last_start_time(data)
                result = True
            else:
                logging.error(f'Timestamp is not stored because in wrong state: {sm.get_current_state().name}')
        elif data[globals.ROLE_KEY] == globals.ROLE_GOAL:
            if sm.get_current_state() == globals.States.RUNNING:
                dh.set_last_goal_time(data)
                result = True
            else:
                logging.error(f'Timestamp is not stored because in wrong state: {sm.get_current_state().name}')
        else:
            logging.error(f'Invalid role: {data[globals.ROLE_KEY]}')
    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Start Server')
    app.run(debug=True, host='0.0.0.0', port=80)

