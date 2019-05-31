#!bin/bash

cd ~/RobotArmWebControl/src/flask_app/assets/

bower install

git clone https://github.com/mrdoob/three.js.git


cd ~/RobotArmWebControl/src/flask_app/
pip3 install -r requirements.txt
