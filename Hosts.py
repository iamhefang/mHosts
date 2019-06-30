import os
import sys

from helpers import ReadText, ReadLines


class Hosts(object):
    __id = None
    __content = ""
    __active = False
    __lines = []
    title = ""

    def __init__(self, title, path):
        self.title = title
        self.__lines = ReadLines(path)
        self.__content = "".join(self.__lines)

    def SetId(self, hostsId):
        self.__id = hostsId

    def GetId(self):
        return self.__id

    def SetActive(self, active=True):
        self.__active = active

    def IsActive(self):
        return self.__active

    def GetLineCount(self):
        return len(self.__lines)

    def save(self):
        """
        保存
        :return: bool
        """
        pass

    def apply(self):
        """
        应用到系统
        :return:
        """
        pass

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
