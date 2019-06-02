#!bin/bash

cd ~/RobotArmWebControl/src/flask_app/assets/

bower install
bower install jquery --save
git clone https://github.com/mrdoob/three.js.git


cd ~/RobotArmWebControl/src/flask_app/
pip3 install --ignore-installed -r requirements.txt
