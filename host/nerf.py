
#!/usr/bin/env python

import cwiid
import time
import serial
import wii
import math
import qik
import os
import socket

motorPort = 8000
periphPort = 8001
host = 'localhost'

q = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q.connect((host, motorPort))

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller.connect((host, periphPort))

sentFlag = 0

'''
Nunchuk
forward:  x,228
back:  x,35
left:  27, x
right:  222,x
middle:  124, 134
'''



def main():
    global sentFlag

    f = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    ip=f.read()

    controller.sendall('ip ' + ip + '\n')
    time.sleep(0.1)
    controller.sendall('wii Scanning...\n')
    print 'Ready to connect...'
    time.sleep(.1)
    wm = None

    while not wm:
        try:
            wm=cwiid.Wiimote()
        except RuntimeError:
            print "Error opening wiimote connection, retrying"

    controller.sendall('wii Connected\n')
    print 'Wii Remote connected...'
    time.sleep(1)

    Rumble = False
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_NUNCHUK

    speed = '128'

    while True:
        button = wm.state['buttons']
    #    print wm.state['nunchuk']['stick']
        stick_y = wm.state['nunchuk']['stick'][1]
        stick_x = wm.state['nunchuk']['stick'][0]

        x = remap(stick_x, 27, 222, -50, 50)
        y = remap(stick_y, 35, 228, -127, 127)
        l_pwm, r_pwm = steer(x, y)

        if l_pwm < 0 :
            l_dir = 1
        else :
            l_dir = 0

        if r_pwm < 0 :
            r_dir = 1
        else :
            r_dir = 0

        l_pwm = abs(l_pwm)
        r_pwm = abs(r_pwm)

        line = str(l_dir) + " " + str(l_pwm) +  " " + str(r_dir) + " " + str(r_pwm) + "\n"
        print line

        q.sendall(line)
        time.sleep(0.1)

        if button == (wii.BTN_PLUS | wii.BTN_MINUS):
            print 'closing Bluetooth connection. Good Bye!'
            time.sleep(1)
            exit(wm)

        if (button == wii.BTN_LEFT) and not(sentFlag & wii.BTN_LEFT):
            print "Left"
            sentFlag = wii.BTN_LEFT
            time.sleep(.5)


        if (button == wii.BTN_UP) and not(sentFlag & wii.BTN_UP) :
            print "forward"
            sentFlag = wii.BTN_UP
            time.sleep(.5)

        if (button  == wii.BTN_RIGHT) and not (sentFlag & wii.BTN_RIGHT):
            print "Right"
            sentFlag = wii.BTN_RIGHT
            time.sleep(.5)

        if (button == wii.BTN_DOWN) and not(sentFlag & wii.BTN_DOWN):
            print "back"
            sentFlag = wii.BTN_DOWN
            time.sleep(.5)
'''
	if (button == wii.BTN_1) :
   	    speed = '255'

	if (button != wii.BTN_1) :
	    speed = '128'

        if (button == 0 ) and not (sentFlag & 8192):
            send('stop1')
            send('stop2')
            sentFlag = 8192
            print "Stop"
'''
def remap (x, in_min, in_max, out_min, out_max) :
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def quit() :
    exit()

def steer (x, y) :
    left_motor = x + y
    right_motor = x - y

    scale_factor = 1

    if abs(left_motor) > 100 or abs(right_motor) > 100:
        x = max(abs(left_motor), abs(right_motor))
        scale_factor = 100.0 / x


    left_motor = int(left_motor * scale_factor) * -1
    right_motor = int(right_motor * scale_factor)

    l = remap(left_motor, -100, 100, -127, 127)
    r = remap(right_motor, -100, 100, -127, 127)

    return l, r



if __name__ == '__main__':
    main()
