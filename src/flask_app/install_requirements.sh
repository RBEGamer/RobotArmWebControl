#!bin/bash
cd ./assets
bower install

cd ./three
git clone https://github.com/mrdoob/three.js.git
cd..
cd ..
pip3 install -r requirements.txt
