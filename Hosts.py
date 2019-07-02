import os
import sys

from helpers import ReadText, WriteText


def Save2System(content):
    return WriteText(GetHostsPath(), content) > 0


def GetHostsPath():
    if sys.platform == "win32":
        return u"%s\\System32\\drivers\\etc\\hosts" % os.environ["WINDIR"]


def GetSystemHosts():
    return ReadText(GetHostsPath())


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
