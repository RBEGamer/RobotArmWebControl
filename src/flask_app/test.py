import json
import os
ABS_PATH = os.path.dirname(
    os.path.abspath(__file__))  # DIRECTORY OF PYTHON APP
print(ABS_PATH)
#LOAD ROBOTS CONFIG FILE
def load_clibration_json(_file):
    jd = {
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
        with open(_file) as json_file:
            data = json.load(json_file)
            #TODO CLEAN
            jd = data
    except:
        print("--- load " + _file + " failed using default")


    return jd

robot_calibration_data  = load_clibration_json(ABS_PATH + "/../arduino_controller/calibration.json")

print(robot_calibration_data)

print(int(robot_calibration_data["AXIS_1_MAX"]))


def math_map(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def map_pot_to_degree(_axis_id, val):
    key_prefix = ""

    if _axis_id == 1:
        key_prefix = "AXIS_1_"
    elif _axis_id == 2:
        key_prefix = "AXIS_2_"
    elif _axis_id == 3:
        key_prefix = "AXIS_3_"
    elif _axis_id == 4:
        key_prefix = "AXIS_4_"
    elif _axis_id == 5:
        key_prefix = "AXIS_5_"
    else:
        return -1


    return int(math_map(val, [
        int(robot_calibration_data[key_prefix + "MIN"])*1.0,
        int(robot_calibration_data[key_prefix + "MAX"])*1.0
    ], [0, int(robot_calibration_data[key_prefix + "TOTAL_DGREE"])*1.0]))


def map_degree_to_pot(_axis_id, val):
    key_prefix = ""

    if _axis_id == 1:
        key_prefix = "AXIS_1_"
    elif _axis_id == 2:
        key_prefix = "AXIS_2_"
    elif _axis_id == 3:
        key_prefix = "AXIS_3_"
    elif _axis_id == 4:
        key_prefix = "AXIS_4_"
    elif _axis_id == 5:
        key_prefix = "AXIS_5_"
    else:
        return -1

    return int(
        math_map(
            val,
            [0,
            int(robot_calibration_data[key_prefix + "TOTAL_DGREE"]) * 1.0], [
                 int(robot_calibration_data[key_prefix + "MIN"]) * 1.0,
                 int(robot_calibration_data[key_prefix + "MAX"]) * 1.0
             ]))


v1 = map_pot_to_degree(1, 128)
v2 = map_degree_to_pot(1, 90)
print(v1)

print(v2)

print(map_pot_to_degree(1, v2))