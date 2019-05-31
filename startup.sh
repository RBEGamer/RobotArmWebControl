cd /home/pi/RobotArmWebControl
#CHECK FOR UPDATE


ssid = $(iw dev | grep ssid | awk '{print $2}')
if [ "$ssid" = "Keunecke 2" ]; then
        git stash save --keep-index --include-untracked  
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$ssid" = "Keunecke" ]; then
        git stash save --keep-index --include-untracked  
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi

if [ "$ssid" = "FRITZBox7362SL" ]; then
        git stash save --keep-index --include-untracked  
        git pull
        bash ./src/rpi_setup_scripts/upload_arduino_sketch.sh
fi


# RUN FLASK APP
bash ./src/flask_app/run_flask_app.sh &





