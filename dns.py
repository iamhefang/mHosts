from socketserver import UDPServer, BaseRequestHandler


class DnsServer:
    __server: UDPServer = None

    def __init__(self, host: str = "0.0.0.0", port: int = 9951):
        self.__server = UDPServer((host, port), DnsRequestHandler)
        pass

    def start(self):
        self.__server.serve_forever()

    def close(self):
        self.__server.server_close()


# todo: 实现dns服务

class DnsRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request[0].strip()
        pass


server = DnsServer()
server.start()
