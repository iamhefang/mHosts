from socket import AF_INET, SOCK_STREAM, socket
from urllib.parse import urlparse


def parseAddr(hostAndPort: str):
    if ":" in hostAndPort:
        (host, port) = hostAndPort.split(":")
    else:
        host = hostAndPort
        port = 80
    return host, int(port)


def parseHttpHeader(rawBytes: bytes):
    headerLines = rawBytes.split(b"\r\n\r\n")[0].decode("utf-8").split("\r\n")
    headers = {}
    for header in headerLines:
        index = headerLines.index(header)
        if index == 0:
            values = header.split(" ")
            if values[0].startswith("HTTP/"):
                headers["http-version"] = values[0]
                headers["code"] = int(values[1])
                headers["message"] = " ".join(values[2:])
            else:
                headers["method"] = values[0]
                headers["url"] = values[1]
                headers["http-version"] = values[2]
        else:
            values = header.split(": ")
            key = values[0].lower()
            if key == "host":
                (host, port) = parseAddr(values[1])
                headers["host"] = host
                headers["port"] = port
            else:
                headers[key] = values[1]
        if "content-length" in headers:
            headers["content-length"] = int(headers["content-length"])
    return headers


def parseResponseBody(rawData: bytes) -> bytes:
    return rawData.split(b"\r\n\r\n")[1]


def makeRequestHeader(option: dict) -> bytes:
    headers = "%s %s %s" % (
        option["method"], option["url"], option["http-version"]
    )
    for key, value in option.items():
        if key == "method" or key == "url" or key == "http-version":
            continue
        headers += "\r\n%s: %s" % (key, value)
    return (headers + "\r\n\r\n").encode("utf-8")


class HttpClient:
    __opt: dict = {
        "method": 'GET',
        "http-version": "HTTP/1.1",
        "connection": "keep-alive",
        "user-agent": "HttpClientPython/1.0.0"
    }

    def __init__(self, option: dict = None):
        self.__opt.update(option if option else {})

    def request(self, url: str):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        address = parseAddr(netloc)
        self.__opt["host"] = netloc
        self.__opt["url"] = url
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(address)
        data = makeRequestHeader(self.__opt)
        client.sendall(data)
        response = client.recv(1024000)
        # while response:
        #     print(response)
        #     response = client.recv(1024)

        resHeaders = parseHttpHeader(response)
        resBody = parseResponseBody(response)
        client.close()
        return resHeaders, resBody


print(HttpClient().request("http://qq.com"))
