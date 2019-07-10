# _*_ coding: utf-8 _*_
import json
import os
import re
import sys
from time import strftime, localtime, time, strptime, mktime
from typing import AnyStr
from urllib import request

from wx import BITMAP_TYPE_PNG, Bitmap

__ResPathCache = {}
__iconCache = {}


def ResPath(path):
    if path not in __ResPathCache:
        __ResPathCache[path] = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path.replace("/", os.sep))
    return __ResPathCache[path]


iconPath = ResPath("icons/logo.ico")


def Now() -> str:
    """
    获取当前时间
    :return:  返回的时间格式为: 2019-07-04 11:11:42
    """
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def Timestamp() -> int:
    """
    获取当前时间戳
    :return:
    """
    return int(time())


def NowToTimestamp(now: str) -> int:
    return int(mktime(strptime(now, "%Y-%m-%d %H:%M:%S")))


def GetIcons() -> dict:
    if not __iconCache:
        iconsPath = ResPath("icons")
        files = os.listdir(iconsPath)
        for file in files:
            if file.endswith(".png"):
                __iconCache[file.split(".")[0]] = Bitmap(ResPath("icons/%s" % file), BITMAP_TYPE_PNG)
    return __iconCache


def FetchNewVersion() -> dict:
    url = "https://raw.githubusercontent.com/iamhefang/mHosts/master/mHosts.json"
    info = json.loads(request.urlopen(url, timeout=10).read().decode('utf-8'), encoding="utf-8")
    return info


def HasPermission(path) -> bool:
    return os.access(path, os.R_OK | os.W_OK)


def ReadText(file, encoding="utf-8") -> str:
    return "".join(ReadLines(file, encoding))


def ReadLines(file, encoding="utf-8") -> list:
    with open(file, mode="r", encoding=encoding, newline="\n") as file:
        return file.readlines()


def WriteText(file: AnyStr, text: AnyStr, encoding="utf-8") -> int:
    with open(file.encode("utf-8"), mode="w", encoding=encoding) as file:
        return file.write(text)


def WriteLines(file, lines, encoding="utf-8"):
    with open(file, mode="w", encoding=encoding) as file:
        file.writelines(lines)


def GetChromePath() -> str:
    path = ""
    if sys.platform == "win32":
        path = u'%(PROGRAMFILES)s\\Google\\Chrome\\Application\\chrome.exe' % os.environ
        if not os.path.exists(path):
            path = u'%s\\Google\\Chrome\\Application\\chrome.exe' % os.environ["PROGRAMFILES(X86)"]
        if not os.path.exists(path):
            path = u"%(LOCALAPPDATA)s\\Google\\Chrome\\Application\\chrome.exe" % os.environ
    elif sys.platform == "linux":
        path = ""
    elif sys.platform == "darwin":
        path = ""
    if not os.path.exists(path):
        path = ""
    return path


def ParseHosts(content: AnyStr) -> str:
    obj = {}
    hosts = []
    lines = content.splitlines()
    lines.reverse()
    for line in lines:
        lineList = re.sub(r' +', ' ', line).split(" ")
        if len(lineList) == 2:
            address = lineList[1].lower()
            if address in obj:
                continue
            obj[address] = lineList[0].strip()
        else:
            obj[line] = ""

    for address, ip in obj.items():
        hosts.append((u"%s %s" % (ip, address)).strip())

    hosts.reverse()
    return os.linesep.join(hosts)
