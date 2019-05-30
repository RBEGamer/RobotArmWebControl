#!bin/bash
cd ./assets
bower install
git clone https://github.com/mrdoob/three.js.git
cd..

pip3 install -r requirements.txt
