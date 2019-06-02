#!bin/python

# INSERT HERE YOUR RPI SERIAL /proc/cpuinfo to automatic get hostname
serdic = {"c31bbd86-84b3-11e9-bc42-526af7764f64":"rawc1",
            "c31bbff2-84b3-11e9-bc42-526af7764f64":"rawc12",
            "c31bc13c-84b3-11e9-bc42-526af7764f64":"rawc3",
            "c31bc4e8-84b3-11e9-bc42-526af7764f64":"rawc4",
            "c31bc63c-84b3-11e9-bc42-526af7764f64":"rawc5"
            ,"0000000015ff1b13":"rawc6",
                        "ERROR000000000":"RAWCDEFAULT",
         "0000000000000000":"RAWCDEFAULT"}

import os



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
hostname = "rawc"
print("RPI_SERIAL")
print(hostname)

#try:
#   hostname = serdic[str(hostname)]
#except:
#    cpuserial = "RAWCDEFAULT"
 
  
print("RPI_NEW_HOSTNAME")
print(hostname)

os.system("sudo hostname -b " + str(hostname))