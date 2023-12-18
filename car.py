import os
import os, struct, array
import time
import os, struct, array
from fcntl import ioctl
import threading
import math
from Rosmaster_Lib import Rosmaster
import os

global servo_x
global servo_y

servo_x=90
servo_y=90

def limit_value(value, minimum, maximum):
    return [value, minimum, maximum].sort()[1]



def move_callback(msg):
    global servo_x,servo_y
    speed_x=-msg["LY"]/32767
    speed_y=-msg["LX"]/32767
    angular_velocity=(msg["LT"]-msg["RT"])/32767/2
    
    servo_dx=-msg["RX"]/32767
    servo_dy=-msg["RY"]/32767
    
    servo_x+=servo_dx
    servo_y+=servo_dy
    
    servo_x=limit_value(servo_x,0,180)
    servo_y=limit_value(servo_y,0,180)
    
    controller.set_car_motion(speed_x,speed_y,angular_velocity)
    controller.set_pwm_servo_all(90,90,servo_x,servo_y)

    print(msg)
    return
        
def shooting_callback(msg):
    

def joystick_thread():
    """
    手柄线程
    """
    print('Available devices:')
    for fn in os.listdir('/dev/input'):
        if fn.startswith('js'):
            print('  /dev/input/%s' % (fn))
    # 这句显示手柄在硬件中的端口位置： /dev/input/js0
    # We'll store the states here.
    axis_states = {
        'LX': 0,
        'LY': 0,
        'RX': 0,
        'RY': 0,
        'LT': 0,
        'RT': 0,
        'XX': 0,
        'YY': 0,
    }
    button_states = {
        'A': 0,
        'B': 0,
        'X': 0,
        'Y': 0,
        'LB': 0,
        'RB': 0,
        'START': 0,
        'BACK': 0,
        'HOME': 0,
        'LO': 0,
        'RO': 0,
    }

    XBOX_TYPE_BUTTON = 0x01
    XBOX_TYPE_AXIS = 0x02

    XBOX_BUTTON_A = 0x00
    XBOX_BUTTON_B = 0x01
    XBOX_BUTTON_X = 0x02
    XBOX_BUTTON_Y = 0x03
    XBOX_BUTTON_LB = 0x04
    XBOX_BUTTON_RB = 0x05
    XBOX_BUTTON_START = 0x06
    XBOX_BUTTON_BACK = 0x07
    XBOX_BUTTON_HOME = 0x08
    XBOX_BUTTON_LO = 0x09    # /* 左摇杆按键 */
    XBOX_BUTTON_RO = 0x0a    # /* 右摇杆按键 */

    XBOX_BUTTON_ON = 0x01
    XBOX_BUTTON_OFF = 0x00

    XBOX_AXIS_LX = 0x00   # /* 左摇杆X轴 */
    XBOX_AXIS_LY = 0x01   # /* 左摇杆Y轴 */
    XBOX_AXIS_RX = 0x03   # /* 右摇杆X轴 */
    XBOX_AXIS_RY = 0x04   # /* 右摇杆Y轴 */
    XBOX_AXIS_LT = 0x02
    XBOX_AXIS_RT = 0x05
    XBOX_AXIS_XX = 0x06    # /* 方向键X轴 */
    XBOX_AXIS_YY = 0x07    # /* 方向键Y轴 */

    XBOX_AXIS_VAL_UP = -32767
    XBOX_AXIS_VAL_DOWN = 32767
    XBOX_AXIS_VAL_LEFT = -32767
    XBOX_AXIS_VAL_RIGHT = 32767

    XBOX_AXIS_VAL_MIN = -32767
    XBOX_AXIS_VAL_MAX = 32767
    XBOX_AXIS_VAL_MID = 0x00

    fn = '/dev/input/js0'
    def xbox_read():
        jsdev = open(fn, 'rb')
        evbuf = jsdev.read(8)
        time, value, type, number = struct.unpack('IhBB', evbuf)
        return [time,value,type,number]

    axis_map = []

    # Open the joystick device.

    jsdev = open(fn, 'rb')

    # # Get the device name.
    buf = array.array('u', ['\0'] * 5)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf)  # JSIOCGNAME(len)
    js_name = buf.tostring()
    print('Device name: %s' % js_name)

    # Get number of axes and buttons.
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf)  # JSIOCGAXES
    num_axes = buf[0]

    # Get the axis map.
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf)  # JSIOCGAXMAP
    # joystick_thread event loop
    while True:
        evbuf = jsdev.read(8)
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)
            if type & 0x01:
                if number == XBOX_BUTTON_A:
                    button_states["A"] = value
                elif number == XBOX_BUTTON_B:
                    button_states["B"] = value
                elif number == XBOX_BUTTON_X:
                    button_states["X"] = value
                elif number == XBOX_BUTTON_Y:
                    button_states["Y"] = value
                elif number == XBOX_BUTTON_LB:
                    button_states["LB"] = value
                elif number == XBOX_BUTTON_RB:
                    button_states["RB"] = value
                elif number == XBOX_BUTTON_START:
                    button_states["START"] = value
                elif number == XBOX_BUTTON_BACK:
                    button_states["BACK"] = value
                elif number == XBOX_BUTTON_HOME:
                    button_states["HOME"] = value
                elif number == XBOX_BUTTON_LO:
                    button_states["LO"] = value
                elif number == XBOX_BUTTON_RO:
                    button_states["RO"] = value
                #print(button_states)
            elif type & 0x02:
                if number == XBOX_AXIS_LX:
                    axis_states["LX"] = value
                elif number == XBOX_AXIS_LY:
                    axis_states["LY"] = value
                elif number == XBOX_AXIS_RX:
                    axis_states["RX"] = value
                elif number == XBOX_AXIS_RY:
                    axis_states["RY"] = value
                elif number == XBOX_AXIS_LT:
                    axis_states["LT"] = value
                elif number == XBOX_AXIS_RT:
                    axis_states["RT"] = value
                elif number == XBOX_AXIS_XX:
                    axis_states["XX"] = value
                elif number == XBOX_AXIS_YY:
                    axis_states["YY"] = value
                #print(axis_states)
            merged_dict = {**axis_states, **button_states}
            move_callback(msg=merged_dict)

if __name__=="__main__":
    controller=Rosmaster(com="/dev/ttyUSB0")
    joystick_thread()