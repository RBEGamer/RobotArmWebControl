#!bin/bash
arduino-cli compile --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/ && arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/

