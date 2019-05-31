#!bin/bash
source ~/.bashrc
cd /home/pi/RobotArmWebControl
#CHECK FOR UPDATE
python ./src/rpi_setup_scripts/check_for_update.py >> ~/Desktop/update_log.txt
# RUN FLASK APP
bash ./src/flask_app/run_flask_app.sh &
