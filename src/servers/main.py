import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen

from src.BackgroundThread import BackgroundThread
from src.settings import Settings


class MainServer(BaseHTTPRequestHandler):
    __thread: BackgroundThread
    __server: HTTPServer

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if self.path == "/apis/hosts/list.json":
            self.wfile.write(json.dumps({
                "success": True,
                "result": Settings.settings["hosts"]
            }).encode())
            return
        matches = re.compile(r"/apis/proxy/(\d+)\.json").match(self.path)
        if matches and matches.group(1):
            hostsId = int(matches.group(1))
            self.wfile.write(json.dumps({
                "success": True,
                "result": {
                    "id": hostsId,
                    "port": 9961
                }
            }).encode())
            return

        self.wfile.write(self.path.encode())

    @staticmethod
    def start():
        try:
            with urlopen("http://127.0.0.1:1994") as res:
                return False
        except:
            def start():
                MainServer.__server = HTTPServer(("127.0.0.1", 1994), MainServer)
                MainServer.__server.serve_forever()

            def stop():
                MainServer.__server.server_close()

            MainServer.__thread = BackgroundThread(start, stop)
            MainServer.__thread.start()
            return True

    @staticmethod
    def stop():
        MainServer.__thread.stop()
