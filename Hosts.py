import os
import sys

from helpers import ReadText


class Hosts(object):
    __id = None
    __content = ""
    __active = False
    title = ""

    def __init__(self, title, path):
        self.title = title
        self.__content = ReadText(path)

    def SetId(self, hostsId):
        self.__id = hostsId

    def GetId(self):
        return self.__id

    def SetActive(self, active=True):
        self.__active = active

    def IsActive(self):
        return self.__active

    @staticmethod
    def GetHostsPath():
        if sys.platform == "win32":
            return u"%s\\System32\\drivers\\etc\\hosts" % os.environ["WINDIR"]

    @staticmethod
    def GetSystemHosts():
        return ReadText(Hosts.GetHostsPath())

    @staticmethod
    def TryFlushDNSCache():
        try:
            if sys.platform == "win32":
                cmd = "ipconfig /flushdns"
            elif sys.platform == "linux":
                cmd = "/etc/init.d/nscd restart"
            elif sys.platform == "mac":
                cmd = "dscacheutil -flushcache"
            else:
                return False
            os.popen(cmd)
            return True
        except Exception:
            return False
