#!/usr/bin/env python
#from threading import Lock
#
#
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json
import os
import smbus2
bus = smbus2.SMBus(1)
DEVICE_ADDRESS = 8


import sys
import time
from flask import Flask, render_template, session, request, redirect, jsonify

async_mode = None
app = Flask(__name__, static_url_path='/assets', static_folder='assets')
app.config['SECRET_KEY'] = 'secret!'



#socketio = SocketIO(app, async_mode=async_mode)
#thread = None
#thread_lock = Lock()


#def background_thread():
#    """Example of how to send server generated events to clients."""
#    count = 0
#    while True:
#        socketio.sleep(10)
#        count += 1
#        socketio.emit('my_response',
#                      {'data': 'Server generated event', 'count': count},
#                      namespace='/test')



@app.route('/assets/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/axis')
def axis():
    id = request.args.get('id')
    dgr = request.args.get('degree')
    print(id, dgr)
    ledout_values = [int(id), int(dgr)]  #send axis_id
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, ledout_values)
    return jsonify(status="ok")


@app.route('/axis_state')
def get_axis_state():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 99, 10)
    print(data)
    return jsonify(status=data)


@app.route('/index.html')
def index_html():
    return redirect('/assets/index.html')


@app.route('/')
def index_root():
    return redirect('/index.html')






if __name__ == '__main__':
    socketio.run(app,host= '0.0.0.0', debug=True)



#@socketio.on('my_event', namespace='/test')
#def test_message(message):
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': message['data'], 'count': session['receive_count']})


#@socketio.on('my_broadcast_event', namespace='/test')
#def test_broadcast_message(message):
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': message['data'], 'count': session['receive_count']},
#         broadcast=True)


#@socketio.on('join', namespace='/test')
#def join(message):
#    join_room(message['room'])
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#        {'data': 'In rooms: ' + ', '.join(rooms()),
#          'count': session['receive_count']})


#@socketio.on('leave', namespace='/test')
#def leave(message):
#    leave_room(message['room'])
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': 'In rooms: ' + ', '.join(rooms()),
#          'count': session['receive_count']})


#@socketio.on('close_room', namespace='/test')
#def close(message):
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                        'count': session['receive_count']},
#         room=message['room'])
#    close_room(message['room'])


#@socketio.on('my_room_event', namespace='/test')
#def send_room_message(message):
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': message['data'], 'count': session['receive_count']},
#         room=message['room'])


#@socketio.on('disconnect_request', namespace='/test')
#def disconnect_request():
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': 'Disconnected!', 'count': session['receive_count']})
#    disconnect()


#@socketio.on('my_ping', namespace='/test')
#def ping_pong():
#    emit('my_pong')


#@socketio.on('connect', namespace='/test')
#def test_connect():
#    global thread
#    with thread_lock:
#        if thread is None:
#            thread = socketio.start_background_task(background_thread)
#    emit('my_response', {'data': 'Connected', 'count': 0})


#@socketio.on('disconnect', namespace='/test')
#def test_disconnect():
#    print('Client disconnected', request.sid)
