from __future__ import annotations

import socket
from threading import Thread
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from typing_extensions import Self


class Client:
    """Socket Client class"""

    ip: str = ""
    port: Optional[int] = None
    _thread: Optional[Thread] = None
    _connected: bool = False

    def __init__(
        self, 
        ip: str, 
        port: int, 
        socket_: socket.socket
    ) -> None:
        self.ip = ip
        self.port = port
        self.socket = socket_
        self._connected = True

    def __repr__(self) -> str:
        return f"<SocketClient-{self.ip}:{self.port}>"

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def address(self) -> tuple[str, int]:
        return (self.ip, self.port)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Client):
            return self.socket == other.socket
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Client):
            return self.socket != other.socket
        return True

    @classmethod
    def connect(cls, ip: str, port: int) -> Optional[Self]:
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            socket_.connect((ip, port))
            
            client = cls(ip, port, socket_)
            client._thread = Thread(target=client.listen_server)
            client._thread.start()
            return client
        except Exception as exc:
            print(exc)
            return None

    def disconnect(self) -> None:
        if not self._connected: return

        self._connected = False
        self.socket.close()

    def listen_server(self) -> None:
        while self._connected:
            try:
                buffer = self.socket.recv(256)
                if not buffer:
                    self.disconnect()
                    break
                
                message = buffer.decode('utf-8')
                print(message)

            except ConnectionResetError:
                self.disconnect()
                break

    def send(self, buffer: bytes) -> None:
        self.socket.sendall(buffer)


if __name__ == "__main__":
    address = input("ip : ")
    if address.count(':'):
        ip = address.split(':')[0]
        port = int(address.split(':')[1])
    else:
        ip = address
        port = int(input("port : "))

    client = Client.connect(ip=ip, port=port)