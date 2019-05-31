#!bin/bash

cd /home/pi/RobotArmWebControl
#CHECK FOR UPDATE


ssid = $(iw dev | grep ssid | awk '{print $2}')
if [ "$ssid" -eq "Keunecke 2" ]; then
   git pull
   bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$ssid" -eq "Keunecke" ]; then
   git pull
   bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$ssid" -eq "FRITZBox7362SL" ]; then
   git pull
   bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

# RUN FLASK APP
bash ./src/flask_app/run_flask_app.sh &
