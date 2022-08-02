from socket import *
import os

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("Waiting to receive messages...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print("Received message: " + data.decode())
    if data.decode() == "exit":
        break
UDPSock.close()
os._exit(0)