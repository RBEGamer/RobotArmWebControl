import os
import shutil
import json

exec_path =os.path.dirname(os.path.abspath(__file__))
print(exec_path)


CONFIG_FILE_DEST_NAME = "calibration.h"


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




def replaceChar(inval, old, new):
    if inval == '':
        return ''
    if inval[0] == old:
        return new + replaceChar(inval[1:], old, new)
    return inval[0] + replaceChar(inval[1:], old, new)


#extracts the serial in the .h files in the config_file folder
def extract_serial_from_config_files(_folder):
    serial_dict = {}
    fs = os.listdir(_folder)
    for fn in fs:
        if "calibration" in str(fn) and str(fn).endswith(".h"):
            #print(fn)
            try:
                f = open(_folder + fn,'r')
                for l in f:
                    l_cleaned = l.replace("#define ", "")
                    l_splitted = l_cleaned.split(" ")
                    if len(l_splitted) != 2:
                        continue
                    if "CPU_CONFIG_SERIAL" in str(l_splitted[0]):
                        #READ SERIAL STRING FROMDEFINE
                        if '\n' in str(l_splitted[1]):
                            l_splitted[1] = str(l_splitted[1]).replace('\n', "")

                        l_splitted[1] = str(l_splitted[1]).replace('"', "")
                        l_splitted[1] = replaceChar(str(l_splitted[1]), " ", "")
                        print(l_splitted[1] + " -> " + fn)
                        serial_dict[str(l_splitted[1])] = fn

                f.close()
            except:
                print("--- cant open file extract_serial_from_config_files " + fn)
                continue
    #print(fs)
    return serial_dict



def parse_calibration_file(_file, _out_json):
    # CREATE A DEFAULT VALUES
    configdict = {
        "AXIS_1_TOTAL_DGREE": 350,
        "AXIS_2_TOTAL_DGREE": 170,
        "AXIS_3_TOTAL_DGREE": 170,
        "AXIS_4_TOTAL_DGREE": 170,
        "AXIS_5_TOTAL_DGREE": 350,
        "AXIS_1_MIN": 0,
        "AXIS_1_MAX": 255,
        "AXIS_2_MIN": 0,
        "AXIS_2_MAX": 255,
        "AXIS_3_MIN": 0,
        "AXIS_3_MAX": 255,
        "AXIS_4_MIN": 0,
        "AXIS_4_MAX": 255,
        "AXIS_5_MIN": 0,
        "AXIS_5_MAX": 255,
    }

    try:
        file = open(_file, "r")
        lines = file.readlines()

        for l in lines:
            # skip comment lines
            if l[0] == '/' and l[1] == '/':
                continue
            #skip empty lines
            if l[0] == '\n':
                continue

            #remove #define
            l_cleaned = l.replace("#define ", "")

            # splite reamining by a whitespace
            l_splitted = l_cleaned.split(" ")

            # skip invalid defines
            if len(l_splitted) != 2:
                continue

            #remove whitespace and new line stuff in key
            if '\n' in str(l_splitted[0]):
                l_splitted[0] = str(l_splitted[0]).replace('\n', "")
            l_splitted[0] = str(l_splitted[0]).replace('"', "")
            l_splitted[0] = replaceChar(str(l_splitted[0]), " ", "")
            #remove whitespace and new line stuff in value
            if '\n' in str(l_splitted[1]):
                l_splitted[1] = str(l_splitted[1]).replace('\n', "")
            l_splitted[1] = str(l_splitted[1]).replace('"', "")
            l_splitted[1] = replaceChar(str(l_splitted[1]), " ", "")

            #print(l_splitted)

            # SET VALUE IN DICT ACCORDING TO THE KEY NAME
            for k, v in configdict.items():
                if k == l_splitted[0]:
                    try:
                        configdict[k] = int(l_splitted[1])
                    except:
                        configdict[k] = l_splitted[1]

                    #print(configdict[k])
                    break

        file.close() # close read file

        config_json = json.dumps(configdict, indent=4)
        print(config_json)

        f = open(_out_json, "w")  #,encoding='utf8'
        f.write(config_json)
        f.close()

    except IOError as x:
        print("cant open " + _file)




print("---------------------")
res = getserial()
print("GOT CPU SERIAL : "+res)
print("---------------------")
file_to_copy = ""
file_ser_dict = extract_serial_from_config_files(exec_path +"/calibration_data/")

try:
    file_to_copy = file_ser_dict[res]  #GET FILE FROM SERIAL
except KeyError as x:
    file_to_copy = "calibration_arm_default.h"






if file_to_copy == "":
    print("INVALID file_to_copy")
    exit(1)

print("---------------------")
print("COPY .h FILE " + exec_path + "/" + file_to_copy)
print("---------------------")

forceCopyFile(exec_path + "/calibration_data/" + file_to_copy,exec_path + "/" + CONFIG_FILE_DEST_NAME)
#CREATE JSON FROM calibration.h for the web app



print("--- CREATING calibration.json ---")
parse_calibration_file(exec_path + "/" + CONFIG_FILE_DEST_NAME, exec_path + "/" + "calibration.json")

print("---------------------")
print("--- END CALIBRATION COPY ---")
print(exec_path + "/" + CONFIG_FILE_DEST_NAME)
print(exec_path + "/" + "calibration.json")
print("---------------------")
print("next step compile the .ino file")