""" TODO :
 - Add command decorators
"""

from __future__ import annotations

import logging
import socket
from threading import Thread
from typing import TYPE_CHECKING, Optional

from utils.enums import BufferType
import utils.logger

if TYPE_CHECKING:
    from typing_extensions import Self
    from server import Server

__log__ = logging.getLogger(__name__)


class Client:
    """Socket Client class"""

    _thread: Optional[Thread] = None
    _connected: bool = False

    def __init__(
        self, 
        ip: Optional[str] = None,
        port: Optional[int] = None,
        socket_: Optional[socket.socket] = None
    ) -> None:
        self.ip = ip
        self.port = port
        self.socket = socket_
        self._connected = True

    def __repr__(self) -> str:
        return f"<SocketClient-{self.ip}:{self.port}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Client) and self.socket == other.socket

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def address(self) -> tuple[str, int]:
        return (self.ip, self.port)

    def _decode(self, buffer: bytes) -> tuple[str, BufferType]:
        message = buffer.decode('utf-8')
        if message.startswith(repr(self)):
            _type = BufferType.system
            message = " ".join(message.split(f"{repr(self)}/")[1:])
        else:
            _type = BufferType.message
        
        return [message, _type]

    @classmethod
    def connect(cls, ip: str, port: int) -> Optional[Self]:
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            socket_.connect((ip, port))

            ip_: str = socket.gethostbyname(socket.gethostname())
            port_: int = socket_.getsockname()[1]
            
            client = cls(ip_, port_, socket_)
            client._thread = Thread(target=client.listen_server)
            client._thread.start()
            return client
        except Exception as exc:
            __log__.exception(exc)
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
                
                message, _type = self._decode(buffer)
                if _type is BufferType.system:
                    __log__.info(message)
                else:
                    print(message)

            except ConnectionResetError:
                if self._connected:
                    __log__.error("Connection was interrupted")
                self.disconnect()
                break

        __log__.info("Disconnected")

    def send_buffer(self, buffer: bytes) -> None:
        if self.is_connected:
            self.socket.sendall(buffer)

    def send_message(self, _message: str) -> None:
        if self.is_connected:
            self.socket.sendall(_message.encode("utf-8"))

    def send_system_message(self, _message: str) -> None:
        if self.is_connected:
            self.socket.sendall(f"{repr(self)}/{_message}".encode("utf-8"))


if __name__ == "__main__":
    address = input("ip : ")
    if address.count(':'):
        ip = address.split(':')[0]
        port = int(address.split(':')[1])
    else:
        ip = address
        port = int(input("port : "))

    client = Client.connect(ip=ip, port=port)
