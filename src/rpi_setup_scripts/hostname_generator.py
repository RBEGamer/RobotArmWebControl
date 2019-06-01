#!bin/python

# INSERT HERE YOUR RPI SERIAL /proc/cpuinfo to automatic get hostname
serdic = {"c31bbd86-84b3-11e9-bc42-526af7764f64":"rawc1",
            "c31bbff2-84b3-11e9-bc42-526af7764f64":"rawc12",
            "c31bc13c-84b3-11e9-bc42-526af7764f64":"rawc3",
            "c31bc4e8-84b3-11e9-bc42-526af7764f64":"rawc4",
            "c31bc63c-84b3-11e9-bc42-526af7764f64":"rawc5"
            ,"c31bc768-84b3-11e9-bc42-526af7764f64":"rawc6"}


import subprocess
from subprocess import Popen, PIPE



def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial
  
  
hostname = getserial();
  
print("RPI_SERIAL")
print(hostname)

hostname = serdic[str(hostname)]

if not hostname:
  hostname = "rawc"
  
print("RPI_NEW_HOSTNAME")
print(hostname)


p1 = Popen(["sudo","hostname", " -b", str(hostname)], stdout=PIPE)

print p1.communicate()
