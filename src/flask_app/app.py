#!/usr/bin/env python
#from threading import Lock
#
#
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json
import os
import smbus2
import threading
from datetime import datetime

import logging
import signal
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as gpio
import sys
import time
from flask import Flask, render_template, session, request, redirect, jsonify
import socket
import fcntl
import struct
import os
from pathlib import Path
from netifaces import interfaces, ifaddresses, AF_INET
from os import walk

abspath = os.path.dirname(os.path.abspath(__file__))

#from RPLCD.i2c import CharLCD
#lcd = CharLCD('PCF8574', 0x27)
#lcd = CharLCD(
#    i2c_expander='PCF8574',
#    address=0x27,
#    port=1,
#    cols=20,
##    rows=4,
#    dotsize=8,
#    charmap='A02',
#    auto_linebreaks=True,
#    backlight_enabled=True)
# SETUP I2C BUS
bus = smbus2.SMBus(1)
DEVICE_ADDRESS = 8  # ADRESS OF THE ARDUINO DUE I2C SLAVE


# LOAD IP ADRESSES FROM ALL INTERFACVES ON THE SYSTEM
ips = {}


def load_ip_adresses_from_interface():
    for ifaceName in interfaces():
        addresses = [
            i['addr'] for i in ifaddresses(ifaceName).setdefault(
                AF_INET, [{
                    'addr': 'No IP addr'
                }])
        ]
        ips[ifaceName] = ''.join(addresses)
load_ip_adresses_from_interface()
print(ips)

# DISPLAY SETTINGS
WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPEED_HZ),
    width=WIDTH,
    height=HEIGHT)

disp.begin()
disp.clear()

# LOAD FONT IN DIFFERENT SIZES
font = ImageFont.load_default()
font_healine = ImageFont.truetype(abspath + '/Retron2000.ttf', 16)
font_small = ImageFont.truetype(abspath + '/Retron2000.ttf', 12)

# SETUP FOR FLASK WEBSERVER
async_mode = None
app = Flask(__name__, static_url_path='/assets', static_folder='assets')
app.config['SECRET_KEY'] = 'secret!'

# SETUP FOR ROBOT ARM PROGRAMS
programs_names = []
programm_running = False
programm_data = []
programm_index = 0
programm_lines = []  # RAW PRG LINES

ABS_PATH = os.path.dirname(os.path.abspath(__file__))  # DIRECTORY OF PYTHON APP


# LOADS ALL .prg PROGRAMM FILES
def get_all_robot_programs_in_dir():
    global programs_names
    files = os.listdir(ABS_PATH)
    programs_names = []
    #print(files)
    for f in files:
        if f.endswith('.prg'):  # LOKK FOR FILES ENDS WITH .prg
            fn = f.replace('.prg', '')
            print(fn)
            programs_names.append(fn)
            print("---ADD PRG ---")


get_all_robot_programs_in_dir()
cursor_index = 0
print(programs_names)

btn_block = False
time_stamp = 0.0
update_disp = False


def button_callback_up(channel):
    global time_stamp  # put in to debounce
    global programm_running
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5:
        print("LOOOL")
        #print "Rising edge detected on port 24 - even though, in the main thread,"
        #print "we are still waiting for a falling edge - how cool?\n"

        if programm_running:
            return
        global cursor_index
        cursor_index = cursor_index + 1
        if cursor_index > (len(programs_names) - 1):
            cursor_index = 0
        if cursor_index < 0:
            cursor_index = 0
        print(cursor_index)
        time.sleep(1)
        print("up")
        #update_display()
        time_stamp = time_now


def button_callback_down(channel):
    #gpio.remove_event_detect(channel)
    global programm_running
    if programm_running:
        return
    global cursor_index
    cursor_index = cursor_index - 1
    if cursor_index < 0:
        cursor_index = 0
    print(cursor_index)
    time.sleep(1)
    print("down")
    #update_display()


def button_callback_ok(channel):
    #gpio.wait_for_edge(12, gpio.RISING)
    global update_disp
    global cursor_index
    global programm_running
    global programm_data
    global programm_index
    global btn_block
    # BLOCK BUTTON PRESS IF PROGRAMM IS PARSED
    if btn_block or programm_running:
        return
    btn_block = True

    #RESET ALL PROGRAMM VARIABLES
    programm_running = False
    programm_data = []
    programm_index = 0
    #GENERATE PROGRAM FILEPATH DEPENDS ON SELECTED ITEM cursor_index
    name = programs_names[cursor_index] + ".prg"
    path = os.path.dirname(os.path.abspath(__file__)) + "/" + name
    print("open " + path)
    #CHECK FILE EXISTS
    my_file = Path(path)
    if my_file.is_file():
        print("FILE READING")
    else:
        print("FILE NOT EXISTS")
    #READ FILE IN; IGNORE COMMENTS LINES; SPLIT AXISX VALUES AND APPEND IT TO THE PROGRAM DICTIONARY
    try:
        with open(path) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                if line.find("#") < 0:  # NO COMMENTS LINE FILTER
                    x = line.split()  #SPLIT FOR WHITESPACE
                    if len(x) == 7:  # LEN CHECK FOR STATEMENTS
                        #print(x)
                        programm_data.append({
                            'axis_0': x[0],
                            'axis_1': x[1],
                            'axis_2': x[2],
                            'axis_3': x[3],
                            'axis_4': x[4],
                            'gripper': x[5],
                            'delay': x[6]
                        })
            fp.close()
        print("-- PRG LOADED ---")
        print(programm_data)
        # PROGRAMM PARSED
        if len(programm_data) > 0:
            programm_running = True
    except:
        pass

    time.sleep(1)
    print("ok")
    update_disp = True
    btn_block = False


def thread_function(name):
    global programm_running
    global programm_data
    global programm_index
    #  global bus
    global update_disp
    thread_step_counter = 0

    while True:
        if programm_running:
            print('--- PRG RUNNING ---')

            pos = programm_data[programm_index]  #GET NEXT INSTRUCTION
            print(pos)

            

            if thread_step_counter > int(pos.get('delay')):
                programm_index = programm_index + 1
                thread_step_counter = 0
                bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[1, int(pos.get('axis_0'))])
                time.sleep(0.1)
                bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[2, int(pos.get('axis_1'))])
                time.sleep(0.1)
                bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[3, int(pos.get('axis_2'))])
                time.sleep(0.1)
                bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[4, int(pos.get('axis_3'))])
                time.sleep(0.1)
                bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[5, int(pos.get('axis_4'))])
                time.sleep(0.1)

            if programm_index >= len(programm_data):  # CHECK PROGRAM FINISHED
                print("-- PRG FINISHED --")
                programm_running = False
                programm_index = 0
                thread_step_counter = 0
                time.sleep(1)
                #update_display()
            #TODO TIMER COUNTER FOR NEXT STEP
            #time.sleep(int(pos.get('delay')))
        time.sleep(2)
        thread_step_counter = thread_step_counter + 1
        #if update_disp:
        #update_display()
        #update_disp =False


program_execution_thread = threading.Thread(target=thread_function, args=(1, ))
program_execution_thread.start()

# SETUP GPIOS TO PULLUP AND EVENT MODE
gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_UP)

# SET EVENTMODE
#gpio.add_event_detect(
#    26, gpio.RISING, callback=button_callback_up, bouncetime=1000)
#gpio.add_event_detect(
#    16, gpio.RISING, callback=button_callback_down, bouncetime=1000)
#gpio.add_event_detect(
#    12, gpio.RISING, callback=button_callback_ok, bouncetime=1000)


# WRITES AN TEXT TO THE DISPLAY BUFFER
def draw_rotated_text(image, text, position, angle, font, fill=(255, 255,
                                                                255)):
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    textimage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    textdraw = ImageDraw.Draw(textimage)  # RENDER TEXT
    textdraw.text((0, 0), text, font=font, fill=fill)
    rotated = textimage.rotate(angle, expand=1)  #ROTATE TEXT IMAGE
    image.paste(rotated, position, rotated)  # INSERT IMAGE TO DISPLAY BUFFER


def update_display():
    global programm_running
    global programm_data
    global programm_index
    global programs_names
    global cursor_index
    global disp

    disp.clear((0, 0, 0))

    draw = disp.draw()

    if not programm_running:
        # DRAW HEADLINE
        draw_rotated_text(
            disp.buffer,
            '--- ROBOT ARM ---', (0, 0),
            90,
            font_healine,
            fill=(0, 255, 255))
        cip = 0
        for key in ips.keys():
            # DRAW IP FOR ETHERNET
            print(key)
            if key == "lo":
                continue
            draw_rotated_text(
                disp.buffer,
                str(key) + ": " + ips[key], (20 + (cip * 10), 10),
                90,
                font_small,
                fill=(255, 0, 255))

        c = 0
        s = ""
        # DRAW THE TEXT FOR EACH PROGRAM
        for name in programs_names:
            # DRAW CURSOR ARROW
            if c == cursor_index:
                s = "-> "
            else:
                s = "   "
    # DRAW PROGRAM NAME WITH Y OFFSET CALCULED THROUGH c
            draw_rotated_text(
                disp.buffer,
                s + name, (55 + (c * 20), 40),
                90,
                font_small,
                fill=(255, 255, 255))

            c = c + 1
    disp.display()


# STATIC WEBSERVER PATH FOR IMAGES AND SCRIPTS
@app.route('/assets/<path:path>')
def static_file(path):
    return app.send_static_file(path)


# API CALL /axisx TO SET AN AXIS
@app.route('/axis')
def axis():
    id = request.args.get('id')
    dgr = request.args.get('degree')
    print(id, dgr)
    try:
        bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00,[int(id), int(dgr)])
        return jsonify(status="ok")
    except :
        return jsonify(status="err")
    # WRITE TO I2C BUS; COMMAND 0 AND AXISX ID AND VALUE



# API CALL TO SET THE GRIPPER STATE
@app.route('/gripper')
def gripper():
    state = request.args.get('state')

    print(state)
    ledout_values = [int(state)]  #send axis_id
    bus.write_i2c_block_data(
        DEVICE_ADDRESS, 0x01,
        ledout_values)  #WRITE TO I2C BUS; COMMAND 1 AND GRIPPER STATE
    return jsonify(status="ok")


# API CALL TO GET STATES FROM ALL AXIS
@app.route('/axis_state')
def get_axis_state():
    global bus
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 99,
                                   15)  #READ I2C BUS 10 INT VALUES
    print(data)
    #update_display()
    return jsonify(status=data)

#GET A LIST OF PARSED PROGRAMS
@app.route('/get_programs')
def get_programs():
    global programs_names
    return jsonify(programs=programs_names)



def load_prg():
    global programm_running
    global programm_data
    global programm_index

    programm_running = False
    programm_data = []
    programm_index = 0
    #GENERATE PROGRAM FILEPATH DEPENDS ON SELECTED ITEM cursor_index
    name = programs_names[cursor_index] + ".prg"
    path = os.path.dirname(os.path.abspath(__file__)) + "/" + name
    print("open " + path)
    #CHECK FILE EXISTS
    my_file = Path(path)
    if my_file.is_file():
        print("FILE READING")
    else:
        print("FILE NOT EXISTS")
    #READ FILE IN; IGNORE COMMENTS LINES; SPLIT AXISX VALUES AND APPEND IT TO THE PROGRAM DICTIONARY
    try:
        with open(path) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                if line.find("#") < 0:  # NO COMMENTS LINE FILTER
                    x = line.split()  #SPLIT FOR WHITESPACE
                    if len(x) == 7:  # LEN CHECK FOR STATEMENTS
                        #print(x)
                        programm_data.append({
                            'axis_0': x[0],
                            'axis_1': x[1],
                            'axis_2': x[2],
                            'axis_3': x[3],
                            'axis_4': x[4],
                            'gripper': x[5],
                            'delay': x[6]
                        })
            fp.close()
        print("-- PRG LOADED ---")
        print(programm_data)
        if len(programm_data) > 0:
            programm_running = True
    except:
        pass



#START A PROGRAM WITH THE GIVEN INDEX
@app.route('/start_program')
def start_program():
    global cursor_index
    id = request.args.get('id')

    cursor_index = int(id)
    load_prg()
    return jsonify(state=id) # TODO

#RETURN THE STATE OF A RUNNING PROGRAM
@app.route('/program_state')
def program_state():
    global programm_running
    global programm_data
    global programm_index
    global programs_names
    global cursor_index
    #id = request.args.get('id')
    return jsonify(
        programm_running=programm_running,
        programm_index=programm_index,
        len=len(programm_data),
        programm_data=programm_data)


@app.route('/stop_program')
def stop_program():
    global programm_running
    programm_running = False
    return jsonify(state=programm_running)  # TODO



# REDIRECT TO STATIC HTML FILE
@app.route('/index.html')
def index_html():
    return redirect('/assets/index.html')


# REDIRECT TO STATIC HTML FILE
@app.route('/')
def index_root():
    return redirect('/index.html')


#update_display()

# STARTUP
if __name__ == '__main__':
    get_all_robot_programs_in_dir()
    # START DISPLAY -> MULTIBLE TIMES TO AVOID PIXEL ERRORS
    time.sleep(2)
    update_display()
    time.sleep(2)
    update_display()
    time.sleep(2)
    update_display()
    # START WEBSERVER
    app.run()
    #socketio.run(app, host='0.0.0.0', debug=True)
