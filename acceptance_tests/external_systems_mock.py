# import flask
# from flask import Flask, request
#
# app = Flask(__name__)
#
# config = {'handshake': True, 'pay': True, 'cancel_payment': True, 'deliver': True, 'cancel_delivery': True}
#
#
# @app.route("/config")
# def set_config():
#     print(request.data.decode())
#
#
# @app.route("/")
# def _():
#     pass
#
#
# app.run(port=80)
import json
import sys
from time import sleep

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

config = {'to_exit': False, 'to_wait': False, 'handshake': True, 'pay': True, 'cancel_payment': True, 'supply': True,
          'cancel_supply': True}
counters = {"supply_counter": 10001, "pay_counter": 10001}
# CORS(app, resources={
#     r"/.*": {
#         "origins": "*",
#         "Content-Type": "application/json"
#     }
# })


@app.route('/config', methods=['post'])
def set_config():
    print("data", request.data)
    dic = json.loads(request.data.decode())
    config.update(dic)
    return 'CONFIG'


@app.route('/', methods=['POST'])
def action():
    print("action", request.data)
    action = json.loads(request.data.decode())
    if config['to_exit']:
        exit()
    if config['to_wait']:
        sleep(6)

    if action['action_type'] == "handshake":
        if config['handshake']:
            return 'OK'
        else:
            return ''

    if action['action_type'] == "pay":
        if config['pay']:
            counters["pay_counter"] += 1
            return str(counters["pay_counter"])
        else:
            return '-1'

    if action['action_type'] == "cancel_pay":
        if config['cancel_pay']:
            return '1'
        else:
            return '-1'

    if action['action_type'] == "supply":
        print(config['supply'])
        if config['supply']:
            counters["supply_counter"] += 1
            return str(counters["supply_counter"])
        else:
            return '-1'

    if action['action_type'] == "cancel_supply":
        if config['cancel_supply']:
            return '1'
        else:
            return '-1'


app.run(port=8080)
