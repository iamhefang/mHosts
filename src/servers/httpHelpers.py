def parseHttpHeader(rawData: bytes):
    data = rawData.decode("utf-8")
    header = data.split("\r\n\r\n")[0].split("\r\n")
    headers = {}
    for line in header:
        index = header.index(line)
        if index == 0:
            value = line.split(" ")
            headers["method"] = value[0]
            headers["url"] = value[1]
            headers["http-version"] = value[2]
        else:
            value = line.split(": ")
            headers[value[0].lower()] = value[1]

    return headers
