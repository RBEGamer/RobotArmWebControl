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
sudo apt-get install python3-pip -y
sudo apt-get install python-pip -y

#INSTALL DISPLAY LIBS
sudo apt install build-essential python3-dev python3-smbus python3-pip python3-numpy git -y
sudo apt-get install -y python-spidev python3-spidev
sudo python3 -m pip install RPi.GPIO
sudo python3 -m pip install Adafruit_GPIO

git clone https://github.com/cskau/Python_ST7735
cd Python_ST7735
sudo python3 setup.py install
cd ~


ls -l /usr/sbin/i2c*

# install mqtt
#sudo apt-get install mosquitto mosquitto-clients -y
sudo apt-get install gcc g++ make
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

# INSTALL NODE
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
npm install bower -g --allow-root
npm install nodemon -g --allow-root


# SETUP STATIC IP
#sudo echo "interface eth0" >> /etc/dhcpcd.conf
#sudo echo "static ip_address=192.168.1.17/24" >> /etc/dhcpcd.conf
#sudo echo "static routers=192.168.1.17" >> /etc/dhcpcd.conf
#sudo echo "static domain_name_servers=192.168.1.17" >> /etc/dhcpcd.conf
#sudo echo "static ip6_address=fd51:42f8:caae:d92e::ff/64" >> /etc/dhcpcd.conf






#USING RELEASES
wget https://github.com/arduino/arduino-cli/releases/download/0.3.6-alpha.preview/arduino-cli-0.3.6-alpha.preview-linuxarm.tar.bz2
tar -xjf ./arduino-cli-0.3.6-alpha.preview-linuxarm.tar.bz2 ########################################################
rm ./arduino-cli-0.3.6-alpha.preview-linuxarm.tar.bz2
cp ./arduino-cli-0.3.6-alpha.preview-linuxarm ./arduino-cli
rm ./arduino-cli-0.3.6-alpha.preview-linuxarm 
sudo chmod +x arduino-cli
sudo cp ./arduino-cli /bin/arduino-cli
#update board list






# install adafruit webide
#curl https://raw.githubusercontent.com/adafruit/Adafruit-WebIDE/master/scripts/install.sh | sudo sh


# GENERATE SSH KEYS



sudo apt-get install git -y
ssh-keygen -t rsa -b 4096 -C "git@prodevmo.com"


cd ~
#anser with yes
echo "-------- ANSWER WITH YES --------------"
git clone https://github.com/RBEGamer/RobotArmWebControl.git

#add autostart

#echo "chmod +x /home/pi/RobotArmWebControl/startup.sh" >> ~/.bashrc
#echo "bash /home/pi/RobotArmWebControl/startup.sh" >> ~/.bashrc

#install python dependencies
cd ~/RobotArmWebControl/src/flask_app



# no sudo needed for npm bower
bash ~/RobotArmWebControl/src/flask_app/install_requirements.sh 
 
sudo pip3 install serial
sudo pip3 install flask-bootstrap
sudo pip3 install flask-socketio
sudo pip3 install smbus2 #REQUIRES SUDO
sudo pip3 install paho-mqtt #REQUIRES SUDO
sudo apt-get install libopenjp2-7 -y #FOR PYTHON PILLOW
sudo apt install libtiff5 -y
sudo apt-get install python3-numpy -y
sudo apt-get install python3-matplotlib -y

# compile arduino sektch
cd ~/RobotArmWebControl/src
arduino-cli core update-index
arduino-cli core install arduino:sam # ARDUINO DUE
arduino-cli core install arduino:avr #ARDUINO UNO MEGA AVR BASED

cd ~/RobotArmWebControl/src/rpi_setup_scripts
bash ./upload_arduino_sketch.sh


#SETTING HOSTNAME
#sudo bash ~/RobotArmWebControl/src/rpi_setup_scripts/sethostname.sh RobotArmCX

#UPDATE CRONTAB
crontab -l > mycron
echo "SHELL=/bin/bash" >> mycron
echo "@reboot /home/pi/RobotArmWebControl/startup.sh > /home/pi/RobotArmWebControl/output.log" >> mycron
crontab mycron
cp mycron ~/crontab_backup
rm mycron




wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap



sudo reboot
