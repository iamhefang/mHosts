from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from src.helpers import WriteText
from src.servers.httpHelpers import parseHttpHeader


class ProxyServer(Thread):
    __server = None
    __conn = None
    __addr = None

    def __init__(self, server, conn, addr):
        Thread.__init__(self, name="ProxyServer")
        self.__server = server
        self.__conn = conn
        self.__addr = addr

    def run(self) -> None:
        # self.run2()
        try:
            data = self.__conn.recv(409600000)
            headers = parseHttpHeader(data)
            client = socket(AF_INET, SOCK_STREAM)
            client.connect(getAddr(headers["host"]))
            client.sendall(data)
            d = client.recv(409600000)
            self.__conn.sendall(d)
        except Exception as e:
            WriteText("error.log", str(e))
            self.__conn.sendall(str(e))
            self.__conn.close()


def getAddr(host):
    a = host.split(":")
    if len(a) == 1:
        return a[0], 80
    else:
        return a[0], int(a[1])


def startProxyServer(port: int = 1994):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(10)
    while True:
        conn, addr = server.accept()
        ProxyServer(server, conn, addr).start()


startProxyServer()
