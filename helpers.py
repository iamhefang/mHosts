# _*_ coding: utf-8 _*_
import os
import sys


def ResPath(path):
    return os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path)


iconPath = ResPath("icons/logo.ico")


def FetchNewVersion():
    pass


def HasPermission(path):
    return os.access(path, os.R_OK | os.W_OK)


def ReadText(file, encoding="utf-8"):
    return "".join(ReadLines(file, encoding))


def ReadLines(file, encoding="utf-8"):
    with open(file, mode="r", encoding=encoding) as file:
        return file.readlines()


def GetChromePath():
    path = None
    if sys.platform == "win32":
        path = u'%s\\Google\\Chrome\\Application\\chrome.exe' % os.environ["PROGRAMFILES(X86)"]
        if not os.path.exists(path):
            path = u'%s\\Google\\Chrome\\Application\\chrome.exe' % os.environ["PROGRAMFILES"]
        if os.path.exists(path):
            path = '"%s"' % path
    elif sys.platform == "linux":
        path = "/opt/chrome/"
    return path
