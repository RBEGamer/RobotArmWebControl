#!/bin/bash
export FLASK_APP=/home/pi/RobotArmWebControl/src/flask_app/app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run --host=0.0.0.0
