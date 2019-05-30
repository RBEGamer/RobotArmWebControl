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

# install arduino ide
cd ~
sudo apt-get install wget -y
wget https://downloads.arduino.cc/arduino-1.8.9-linuxaarch64.tar.xz
tar -xf  arduino-1.8.9-linuxaarch64.tar.xz 
cd arduino-1.8.9/
bash ./setup.sh
cd ~
rm arduino-1.8.9-linuxaarch64.tar.xz

# install arduino cli
sudo apt install golang -y
export PATH=/usr/local/go/bin:$PATH
echo "export PATH=/usr/local/go/bin:$PATH" >> ~/.bashrc
export GOPATH=$HOME/go
echo "export GOPATH=$HOME/go" >> ~/.bashrc
export PATH=$PATH:$GOPATH/bin
echo "export PATH=$PATH:$GOPATH/bin" >> ~/.bashrc


#USING RELEASES
wget https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2
tar -xjf arduino-cli-latest-linuxarm.tar.bz2 
rm arduino-cli-latest-linuxarm.tar.bz2
sudo chmod +x arduino-cli
sudo cp ./arduino-cli /bin/arduino-cli
#update board list
arduino-cli core update-index
#install samd arduino due plattform
arduino-cli core install arduino:samd
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
echo "-------- SELECT OPTION 2 FOR NANO EDITOR --------------"
echo "----- ADD @reboot bash /home/pi/RobotArmWebControl/startup.sh ------"
crontab -e 


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
