#!bin/bash
cd ~

sudo apt-get update
sudo apt-get upgrade -y


#install i2c
adduser pi i2c
adduser www-data i2c

sudo apt-get install i2c-tools -y
sudo apt-get install python-smbus -y
sudo apt-get install libi2c-dev -y
ls -l /usr/sbin/i2c*

# install mqtt
sudo apt-get install mosquitto mosquitto-clients -y

# install arduino cli
cd ~
sudo apt install golang -y
export PATH=/usr/local/go/bin:$PATH
echo "export PATH=/usr/local/go/bin:$PATH" >> ~/.bashrc
export GOPATH=$HOME/go
echo "export GOPATH=$HOME/go" >> ~/.bashrc
export PATH=$PATH:$GOPATH/bin
echo "export PATH=$PATH:$GOPATH/bin" >> ~/.bashrc
#TODO COPY
#TODO EXC




# SETUP STATIC IP
sudo echo "interface eth0" >> /etc/dhcpcd.conf
sudo echo "static ip_address=192.168.1.1/24" >> /etc/dhcpcd.conf
sudo echo "static routers=192.168.1.1" >> /etc/dhcpcd.conf
sudo echo "static domain_name_servers=192.168.1.1" >> /etc/dhcpcd.conf





#USING RELEASES
wget https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2
tar -xjf arduino-cli-latest-linuxarm.tar.bz2 
rm arduino-cli-latest-linuxarm.tar.bz2
sudo chmod +x arduino-cli
sudo cp ./arduino-cli /bin/arduino-cli
#update board list
arduino-cli core update-index
#install samd arduino due plattform
arduino-cli core install arduino:samd #mkr100
arduino-cli core install arduino:sam #due
arduino-cli core install arduino:avr #mega
#check if board detected
arduino-cli board list





# install adafruit webide
curl https://raw.githubusercontent.com/adafruit/Adafruit-WebIDE/master/scripts/install.sh | sudo sh


# GENERATE SSH KEYS
sudo apt-get install xclip -y
echo "alias pbcopy='xclip -selection clipboard'" >> ~/.bashrc
echo "alias pbpaste='xclip -selection clipboard -o'" >> ~/.bashrc
source ~/.bashrc


sudo apt-get install git
ssh-keygen -t rsa -b 4096 -C "git@prodevmo.com"


cd ~
#anser with yes
echo "-------- ANSWER WITH YES --------------"
git clone git@github.com:RBEGamer/RobotArmWebControl.git 

#add autostart

echo "chmod +x /home/pi/RobotArmWebControl/startup.sh" >> ~/.bashrc
echo "bash /home/pi/RobotArmWebControl/startup.sh" >> ~/.bashrc

#install python dependencies
cd ~/RobotArmWebControl/src/flask_app

sudo npm install bower -g
sudo npm install nodemon -g


sudo  ./bash install_requirements.sh 
 
sudo pip install flask-bootstrap
sudo pip install serial
sudo pip install GitPython
sudo pip install flask-bootstrap
sudo pip install serial

sudo pip3 install flask-socketio
sudo pip3 install smbus2
sudo pip3 install paho-mqtt


# compile arduino sektch
#compile arduino sketch
cd ~/RobotArmWebControl/src/
arduino-cli board list
arduino-cli compile --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:sam:arduino_due_x_dbg ./arduino_controller/
