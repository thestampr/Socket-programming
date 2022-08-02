from socket import *
import os

def client():
    while True:
        connect = input("Connect to : ")
        if connect == '' :
            os._exit(0)
        host = connect.split(":")[0]
        port = connect.split(":")[-1]
        print("Connecting...",end="                     \r")
        try:
            addr = (host, int(port))
            UDPSock = socket(AF_INET, SOCK_DGRAM)
            UDPSock.sendto(str("/connect").encode(), addr)
            print("Connected",end="                        \n")
        except:
            print("Unknow address.")
            client()
        while True:
            data = input(">")
            if data.lower() == "/exit":
                UDPSock.sendto(str("/disconnect").encode(), addr)
                UDPSock.close()
                os._exit(0)
            elif data.lower() == "/disconnect":
                UDPSock.sendto(str("/disconnect").encode(), addr)
                print("Disconnected")
                UDPSock.close()
                break
            UDPSock.sendto(data.encode(), addr)

client()