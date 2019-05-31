#!bin/bash

cd /home/pi/RobotArmWebControl
#CHECK FOR UPDATE


SSID=`iw dev | grep ssid | awk '{print $2}'`
echo "$SSID"
if [ "$SSID" = "Keunecke2" ]; then
        echo "UP"
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$SSID" = "Keunecke" ]; then
        echo "UPDATE"
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$SSID" = "FRITZBox7362SL" ]; then
        echo "UPDATE"   
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

# RUN FLASK APP
bash ./src/flask_app/run_flask_app.sh &







