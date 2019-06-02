# RobotArmWebControl


#TODO IMAGE








# INSTALL A FRESH RPI
* install a fresh raspbian

Run `raspi-config` and change the following things
* setup a wifi-country, setup a wifi
* `interfacing options -> I2C -> ENABLE`
* `interfacing options -> Serial -> Serial Console NO -> Enabled -> YES`
* `reboot`

finally to install the RobotArmSoftware run :
* `cd ~`
* `curl https://raw.githubusercontent.com/RBEGamer/RobotArmWebControl/master/src/rpi_setup_scripts/setup_base.sh | sudo sh`
