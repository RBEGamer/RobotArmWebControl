import os
import shutil

exec_path =os.path.dirname(os.path.abspath(__file__))
print(exec_path)


def getserial():
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

def forceCopyFile (sfile, dfile):
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)

res = getserial()
print(res)
file_to_copy = ""
if res == "000000008b443c09": #C1 ROBOT ARM
    file_to_copy = "calibration_arm_c1.h"
elif res == "00000000caeca7c3":
    file_to_copy = "calibration_arm_c2.h"
elif res == "00000000d3063ddc":
    file_to_copy = "calibration_arm_c3.h"


if file_to_copy == "":
  print("INVALID SERIAL")
  exit(1)
print(exec_path + "/" + file_to_copy)
forceCopyFile(exec_path + "/calibration_data/" + file_to_copy,
              exec_path + "/calibration.h")
print("--- END CALIBRATION COPY ---")
