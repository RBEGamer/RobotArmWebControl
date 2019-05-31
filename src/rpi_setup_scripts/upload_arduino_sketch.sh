#!bin/bash

cd ~/RobotArmWebControl/src/

if [ ! -f ./arduino_controller/arduino_controller.ino ]; then

echo "-- UPLOADING TO ARDUINO --"
arduino-cli board list
arduino-cli compile --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/
echo "-- END UPLOADING TO ARDUINO --"

else

echo " -- no arduino_controller.ino in dir --"

fi

