import logging
from flask import Flask, request

import datahandler

app = Flask(__name__)
dh = datahandler.DataHandler()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the data
        logging.info(f'Received POST request with data: {data}')
        dh.save_timestamp(data)
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

