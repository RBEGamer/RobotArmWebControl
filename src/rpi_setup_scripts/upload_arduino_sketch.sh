#!bin/bash

cd /home/pi/RobotArmWebControl/src/

#if [ ! -f /home/pi/RobotArmWebControl/src/arduino_controller/arduino_controller.ino ]; then
echo "-- COPY CALIBRATION DATA"

python /home/pi/RobotArmWebControl/src/arduino_controller/calibration_data_copier.py

echo "-- UPLOADING TO ARDUINO --"
arduino-cli board list
arduino-cli compile --fqbn arduino:sam:arduino_due_x_dbg /home/pi/RobotArmWebControl/src/arduino_controller/
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:sam:arduino_due_x_dbg /home/pi/RobotArmWebControl/src/arduino_controller/
echo "-- END UPLOADING TO ARDUINO --"

#else

#echo " -- no arduino_controller.ino in dir --"

#fi

