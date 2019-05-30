# RobotArmWebControl
for bachelor thesis from Lotte


#TODO IMAGE




# TODO HARDWARE





# TODO PCB AND PARTLIST








# EXPORT 3D MODEL

The 3d format is used in the webapp is `OBJ`. In Autodesk Inventor use `EXPORR CAD` -> `OBJ` -> `Options` -> `Export Unit Zentimeter`.

The Models must be placed in the Models-Folder of the WebApp `./src/flask_app/assets/3d_models/`


* RobotBox/Base -> `base_box.obj` and for texture `base_box.mtl`


# INSTALL A FRESH RPI
* install a fresh raspbian
* change the hostname
* install updates
* setup a wifi

to install all software run :
`curl https://raw.githubusercontent.com/RBEGamer/RobotArmWebControl/master/src/rpi_setup_scripts/setup_base.sh | sudo sh`
