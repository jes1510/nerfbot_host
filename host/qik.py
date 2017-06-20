import serial

forward = 0
reverse = 1

import time


class Parameters :
    def __init__(self) :
        self.deviceID = 0
        self.PWM = 1
        self.shutDownonError = 2
        self.timeout = 3
        self.M0Acceleration = 4
        self.M1Acceleration = 5
        self.M0Brake = 6
        self.M1Brake = 7
        self.M0CurrentLimit = 8
        self.M1CurrentLimit = 9
        self.M0CurrentLimitResponse = 10
        self.M1CurrentLimitResponse = 11


class Commands :
    def __init__(self) :
        self.MOForward = 0x88
        self.M0Forward8bit = 0x89
        self.M0Reverse = 0x8a
        self.M0Revers8Bit = 0x8b

        self.M1Forward = 0x8C
        self.M1Forward8bit = 0x8D
        self.M1Reverse = 0x8E
        self.M1Revers8Bit = 0x8F

        self.set = 0x84
        self.get = 0x83

        self.M0Brake = 0x86
        self.M1Brake = 0x87

        self.getM0Current = 0x90
        self.getM1Current = 0x91

        self.getM0Speed = 0x92
        self.getM1Speed = 0x93

class Errors :
    def __init__ ( self) :
        self.motor0 = 0
        self.motor1 = 2
        self.motor0OverCurrent = 4
        self.motor1OverCurrent = 8
        self.serialHardware = 16
        self.CRC = 32
        self.format = 64
        self.timeout = 128

        self.OK = 0
        self.badParameter = 1
        self.badValue = 2





class Qik :
    def __init__ (self, port, baud):
        self.port = port
        self.baud = baud

        self.port = serial.Serial(self.port, self.baud)
                #Allows autobaud
        self.port.write(chr(0xAA))
        self.commands = Commands()
        self.errors = Errors()
        self.parameters = Parameters

    def send(self, command) :
        self.port.write(chr(command))

    def moveM0(self, direction, speed) :
        if direction == forward :
            self.send(self.commands.MOForward)
        else :
            self.send(self.commands.M0Reverse)
        self.send(speed)

    def set(self, parameter, value) :
        self.send(self.commands.set)
        self.send(parameter)
        self.send(value)
        self.send(0x55)
        self.send(0x2A)
        time.sleep(0.1)
        return self.port.read(1)

    def moveM1(self, direction, speed) :
        if direction == forward :
            self.send(self.commands.M1Forward)
        else :
            self.send(self.commands.M1Reverse)
        self.send(speed)


    def getVer(self) :
        self.send(0x81)
        return self.port.read(1)

if __name__ == '__main__' :
#print ser.read(1)
    q = Qik('/dev/ttyUSB0', 9600)
    #q.run()

    p = Parameters()
    print "Firmware Version: " + str(q.getVer())
    #print "Accel: ", str(q.set(p.M1Acceleration, 0x40))
    q.moveM0(forward, 0x00)
    q.moveM1(forward, 0x00)
