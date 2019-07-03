# _*_ coding: utf-8 _*_
import json
import os
import sys
from urllib import request

from wx import BITMAP_TYPE_PNG, Bitmap

__ResPathCache = {}
__iconCache = {}


def ResPath(path):
    if path not in __ResPathCache:
        __ResPathCache[path] = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path.replace("/", os.sep))
    return __ResPathCache[path]


iconPath = ResPath("icons/logo.ico")


def GetIcons() -> dict:
    if not __iconCache:
        iconsPath = ResPath("icons")
        files = os.listdir(iconsPath)
        for file in files:
            if file.endswith(".png"):
                __iconCache[file.split(".")[0]] = Bitmap("icons/%s" % file, BITMAP_TYPE_PNG)
    return __iconCache


def FetchNewVersion():
    url = "https://raw.githubusercontent.com/iamhefang/mHosts/master/mHosts.json"
    info = json.loads(request.urlopen(url, timeout=10).read().decode('utf-8'), encoding="utf-8")
    return info


def HasPermission(path):
    return os.access(path, os.R_OK | os.W_OK)


def ReadText(file, encoding="utf-8"):
    return "".join(ReadLines(file, encoding))


def ReadLines(file, encoding="utf-8"):
    with open(file, mode="r", encoding=encoding) as file:
        return file.readlines()


def WriteText(file, text, encoding="utf-8"):
    with open(file, mode="w+", encoding=encoding) as file:
        return file.write(text)


def WriteLines(file, lines, encoding="utf-8"):
    with open(file, mode="w+", encoding=encoding) as file:
        return file.writelines(lines)


def GetChromePath():
    path = None
    if sys.platform == "win32":
        path = u'%s\\Google\\Chrome\\Application\\chrome.exe' % os.environ["PROGRAMFILES(X86)"]
        if not os.path.exists(path):
            path = u'%s\\Google\\Chrome\\Application\\chrome.exe' % os.environ["PROGRAMFILES"]
        # if os.path.exists(path):
        #     path = '"%s"' % path
    elif sys.platform == "linux":
        path = "google-chrome"
    return path
