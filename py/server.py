from __future__ import annotations

import logging
import socket
from threading import Thread
from typing import TYPE_CHECKING, Optional

import utils.logger
from client import Client

if TYPE_CHECKING:
    from typing_extensions import Self

__log__ = logging.getLogger(__name__)


class Server:
    """Socket Server class"""

    ip: str = socket.gethostbyname(socket.gethostname()) # 127.0.0.1

    clients: list[Client] = []
    _thread: Optional[Thread] = None

    def __init__(self, port: int, buffer: int = 1024) -> None:
        self.port = port
        self.buffer = buffer
        
        self._runing: bool = False

    def __repr__(self) -> str:
        return f"<SocketServer-{self.ip}:{self.port}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Server) and self.socket == other.socket

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def address(self) -> tuple[str, int]:
        return (self.ip, self.port)

    def start(self) -> None:
        self._runing = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(5)

        self._thread = Thread(target=self.listening, daemon=True)
        self._thread.start()

    def run(self) -> None:
        self._runing = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(5)

        self.listening()

    def stop(self) -> None:
        self._runing = False
        self.cleanup()

        if self._thread:
            self._thread.join()
            self._thread = None

    def streaming(self, buffer: bytes, sender: Client) -> None:
        for client in self.clients:
            if client != sender and client.is_connected:
                client.send_buffer(buffer)

    def listening(self) -> None:
        __log__.info(f"{repr(self)} ready")

        while self._runing:
            socket_, (ip, port) = self.socket.accept()
            if not self._runing: break

            client = self.add_client(ip=ip, port=port, socket_=socket_)
            if client:
                _t = Thread(target=self.listen_client, args=(client,), daemon=True)
                _t.start()

    def listen_client(self, client: Client) -> None:
        __log__.info(f"{repr(client)} Connected")
        client.send_system_message(f"Connected to {repr(self)}")

        while self._runing and client.is_connected:
            try:
                buffer = client.socket.recv(256)
                if not buffer:
                    client.disconnect()
                    break
                self.streaming(buffer=buffer, sender=client)
            except ConnectionResetError:
                client.disconnect()
                break

        __log__.info(f"{repr(client)} Disconnected")

    def add_client(self, ip: str, port: int, socket_: socket.socket) -> Optional[Client]:
        client = Client(ip=ip, port=port, socket_=socket_)

        if client not in self.clients:
            self.clients.append(client)
            return client
        else:
            return None

    def remove_client(self, client: Client) -> bool:
        if client in self.clients:
            client.disconnect()
            self.clients.remove(client)
            return True
        else:
            return False

    def cleanup(self) -> None:
        for client in self.clients:
            client.disconnect()
        self.clients.clear()


if __name__ == "__main__":
    try:
        port = int(input("port : "))
        server = Server(port=port)
        server.run()
    except ValueError:
        ...
