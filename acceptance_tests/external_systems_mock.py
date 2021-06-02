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
app = Flask(__name__)

config = {'to_exit': False, 'to_wait': False, 'handshake': True, 'pay': True, 'cancel_payment': True, 'supply': True, 'cancel_supply': True}
supply_counter = 10001
pay_counter = 10001

@app.route('/config', methods=['post'])
def set_config():
    dic = request.data.decode()
    if 'to_exit' in dic:
        config['to_exit'] = dic['to_exit']
    if 'to_wait' in dic:
        config['to_wait'] = dic['to_wait']
    if 'handshake' in dic:
        config['handshake'] = dic['handshake']
    if 'pay' in dic:
        config['pay'] = dic['pay']
    if 'cancel_payment' in dic:
        config['cancel_payment'] = dic['cancel_payment']
    if 'deliver' in dic:
        config['deliver'] = dic['deliver']
    if 'cancel_delivery' in dic:
        config['cancel_delivery'] = dic['cancel_delivery']

    return 'CONFIG'


@app.route('/')
def action():
    action = request.data.decode()
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
            pay_counter += 1
            return pay_counter
        else:
            return '-1'

    if action['action_type'] == "cancel_pay":
        if config['cancel_pay']:
            return '1'
        else:
            return '-1'

    if action['action_type'] == "supply":
        if config['supply']:
            supply_counter += 1
            return supply_counter
        else:
            return '-1'

    if action['action_type'] == "cancel_supply":
        if config['cancel_supply']:
            return '1'
        else:
            return '-1'



app.run(port=5000)
