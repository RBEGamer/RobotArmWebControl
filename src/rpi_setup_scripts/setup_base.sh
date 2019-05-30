#!bin/bash
cd ~

#install i2c
adduser pi i2c
adduser www-data i2c

sudo apt-get install i2c-tools
sudo apt-get install python-smbus
sudo apt-get install libi2c-dev
ls -l /usr/sbin/i2c*

# install arduino ide
cd ~
sudo apt-get install wget
wget https://downloads.arduino.cc/arduino-1.8.9-linuxaarch64.tar.xz
tar -xf  arduino-1.8.9-linuxaarch64.tar.xz 
cd arduino-1.8.9/
bash ./setup.sh
cd ~
rm arduino-1.8.9-linuxaarch64.tar.xz



sudo pip install flask-bootstrap
sudo pip install serial

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
echo "-------- SELECT OPTION 2 FOR NANO EDITOR --------------"
echo "----- ADD @reboot bash /home/pi/RobotArmWebControl/startup.sh ------"
crontab -e 
