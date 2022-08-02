from socket import *
import os

host = input("Connect to : ")
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = input(">")
    UDPSock.sendto(data.encode(), addr)
    if data.lower() == "exit":
        break
UDPSock.close()
os._exit(0)