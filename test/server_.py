import socket

host = ""
port = 13000
buf = 1024

print("IP : " + socket.gethostbyname(socket.gethostname()) + ":" + str(port))

from socket import *
from threading import Thread
import keyboard
import time
import os

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

def network():
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        if data.decode().lower() == "/connect":
            print(str(addr).split("'")[1] + ":Connected")
        elif data.decode().lower() == "/disconnect":
            print(str(addr).split("'")[1] + ":Disconnected")
        else:
            if data.decode().lower() == "":
                pass
            else:
                print(str(addr).split("'")[1] + ":COMMAND:" + data.decode())
            keyboard.press_and_release('ctrl+alt+c')
            time.sleep(0.1)
            keyboard.write(data.decode())
            keyboard.press_and_release('enter')

Thread(target = network, daemon = True).start()

while True:
    command = input()
    if command == "/disconnect":
        print("Disconnected")
        UDPSock.close()
        os._exit(0)