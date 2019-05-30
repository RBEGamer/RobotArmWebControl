#!bin/bash

#CHECK FOR UPDATE
python ./src/rpi_setup_scripts/check_for_update.py



bash ./src/flask_app/run_flask_app.sh &
