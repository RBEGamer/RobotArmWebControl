#!bin/bash

cd ~/RobotArmWebControl/src/flask_app/assets/

bower install

git clone https://github.com/mrdoob/three.js.git

cd..

pip3 install -r requirements.txt
