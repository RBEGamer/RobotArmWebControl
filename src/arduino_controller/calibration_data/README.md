# CALIBRATION_DATA DIRECTORY

This dir contains the calibration data for each robot arm build.

The suffix `C1`, `C2`,.. are the build numbers on the robots.

A .h file contain information about the endstop and the stepper pin config.
The file will be copied by the `calibration_data_copier.py` script.

To  add a new robot calibration file, create a new .h file and use the template from the 
`calibration_arm_default.h`.

Change the  `#define CPU_CONFIG_SERIAL "ERROR00000000000"` to the serial number of the PI.

See `/proc/cpuinfo` for the pi serial number.

