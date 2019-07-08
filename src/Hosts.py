import os
import sys

from src.helpers import ReadText, WriteText


def Save2System(content):
    return WriteText(GetHostsPath(), content) > 0


def GetHostsPath():
    if sys.platform == "win32":
        return u"%s\\System32\\drivers\\etc\\hosts" % os.environ["WINDIR"]
    elif sys.platform == "linux":
        return u"/etc/hosts"
    elif sys.platform == "darwin":
        return u"/private/etc/hosts"


def GetSystemHosts():
    return ReadText(GetHostsPath())


def SetDnsServer(address: str = "127.0.0.1"):
    """
    设置dns服务器
    :param address: 要设置的dns地址
    :return:
    """
    if sys.platform == "darwin":
        # subprocess.Popen("networksetup -setdnsservers ")
        pass
        # networksetup -setdnsservers Wi-Fi 8.8.8.8
    elif sys.platform == "win32":
        pass
    elif sys.platform == "linux":
        pass
    pass


def TryFlushDNSCache():
    try:
        if sys.platform == "win32":
            cmd = "ipconfig /flushdns"
        elif sys.platform == "linux":
            cmd = "/etc/init.d/nscd restart"
        elif sys.platform == "darwin":
            cmd = "dscacheutil -flushcache"
        else:
            return False
        os.system(cmd)
        return True
    except:
        return False
