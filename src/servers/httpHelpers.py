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
        if not header:
            continue
        index = headerLines.index(header)
        if index == 0:
            values = header.split(" ")
            if values[0].startswith("HTTP/"):
                headers["Http-version"] = values[0]
                headers["Code"] = int(values[1])
                headers["Message"] = " ".join(values[2:])
            else:
                headers["Method"] = values[0]
                headers["Url"] = values[1]
                headers["Http-Version"] = values[2]
        else:
            values = header.split(": ")
            key = values[0].lower()
            if key == "Host":
                (host, port) = parseAddr(values[1])
                headers["Host"] = host
                headers["Port"] = port
            else:
                headers[key] = values[1]
        if "Content-Length" in headers:
            headers["Content-Length"] = int(headers["Content-Length"])
    return headers


def parseResponseBody(rawData: bytes) -> bytes:
    return rawData.split(b"\r\n\r\n")[1] if b"\r\n\r\n" in rawData else None


def makeRequestHeader(option: dict) -> bytes:
    headers = "%s %s %s" % (
        option["Method"], option["Url"], option["Http-Version"]
    )
    for key, value in option.items():
        if key == "Method" or key == "Url" or key == "Http-Version":
            continue
        headers += "\r\n%s: %s" % (key, value)
    return (headers + "\r\n\r\n").encode("utf-8")


class HttpClient:
    __opt: dict = {
        "Method": 'GET',
        "Http-Version": "HTTP/1.1",
        "Connection": "keep-alive",
        "User-Agent": "HttpClientPython/1.0.0"
    }

    def __init__(self, option: dict = None):
        self.__opt.update(option if option else {})

    def request(self, url: str):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        address = parseAddr(netloc)
        self.__opt["Host"] = netloc
        self.__opt["Url"] = url
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


print(HttpClient().request("http://10.8.241.47:8000/api/v1/Amon/UnitTemplate/"))
