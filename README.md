
![Gopher image](/logo.png)










# INSTALL A FRESH RPI
* install a fresh raspbian

Run `raspi-config` and change the following things
* setup a wifi-country, setup a wifi
* `interfacing options -> I2C -> ENABLE`
* `interfacing options -> Serial -> Serial Console NO -> Enabled -> YES`
* `locationsation options -> set wifi country`
* `network options -> set hostname`
* `network options -> connect to a wifi`
* `locationsation options -> generate locale`
* `reboot`



finally to install the RobotArmSoftware run :
# THE USER HAS TO BE PI AND ITS HOME DIRECTORY /HOME/PI/
* `cd /home/pi`
* `wget https://raw.githubusercontent.com/RBEGamer/RobotArmWebControl/master/src/rpi_setup_scripts/setup_base.sh && sudo chmod +x ./setup_base.sh  && sudo bash ./setup_base.sh && rm ./setup_base.sh`
