'''
    Server for communicating with peripherals and motors
'''

import socket
import sys
from thread import *
import serial
import select
import qik
import time

host = ''
motorPort = 8000
periphPort = 8001

periphSer = serial.Serial('/dev/ttyACM0', 9600)
q = qik.Qik('/dev/ttyUSB0', 9600)

motorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
periphSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stopMain = False


try:
    motorSocket.bind((host, motorPort))
    periphSocket.bind((host, periphPort))
    motorSocket.setblocking(0)
    periphSocket.setblocking(0)

except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


motorSocket.listen(4)
periphSocket.listen(4)

inputs = [motorSocket, periphSocket]
outputs = []


def clientthread(conn):
    global stopMain
    conn.send('Ready\n')

    while True :     #  Loop until empty or "quit"
        add, port = conn.getsockname()

        data = conn.recv(1024)
        print "RCVD : " + data + "\tFrom:", add, port
        if not data :
            break

        if data.strip() == "end" :
            print "Ending thread!"
            conn.send("Goodbye!")
            conn.close()
            break


        if data.strip() == "quit" or data.strip() == "exit":
            conn.send("Goodbye!")
            stopMain = True
            conn.close()
            break


        if port == motorPort :
            try :
                data = data.strip()
                splitData = data.split(' ')
                m1dir, m1pwm, m2dir, m2pwm = splitData
                q.moveM0(int(m1dir), int(m1pwm))
                #port.send(periphSer.readline())
                q.moveM1(int(m2dir), int(m2pwm))
                #port.send(periphSer.readline())

            except :
                print "Corrupt Frame!"
                conn.send("Corrupt Frame")

        if port == periphPort :
            periphSer.write(data + '\n')
            returned = periphSer.readline()

            if returned.strip() != "OK" :
                print periphSer.readline()

            conn.send(returned)        

    conn.close()

count = 0

while not stopMain:
    readable, writable, exceptional = select.select(inputs, inputs, inputs, 3)
    if readable :
        for s in readable :
            conn, add = s.accept()
            print s.getsockname()
            start_new_thread(clientthread ,(conn,))


s.close()
