#!bin/python

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


  
p1 = Popen(["sudo","hostname", " -b", str(hostname)], stdout=PIPE)

print p1.communicate()
