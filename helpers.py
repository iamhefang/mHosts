# _*_ coding: utf-8 _*_
import json
import os
import sys
from urllib import request


def ResPath(path):
    return os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path)


iconPath = ResPath("icons/logo.ico")


def FetchNewVersion():
    url = "https://raw.githubusercontent.com/iamhefang/mHosts/master/mHosts.json"
    info = json.loads(request.urlopen(url).read().decode('utf-8'), encoding="utf-8")
    return info['version']


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
