# _*_ coding: utf-8 _*_
import sys

import wx

from src.servers.main import MainServer
from src.settings import Settings
from src.views.MainWindow import MainWindow

if __name__ == '__main__':
    if not MainServer.start():
        app = wx.App()
        wx.MessageBox("程序正在运行中, 请勿重复打开", "正在运行", wx.ICON_ERROR)
        app.Destroy()
    else:
        Settings.Init()
        if sys.platform == "win32":
            # 开启在Windows系统中高分屏适配
            # 方案来自 https://groups.google.com/forum/#!topic/wxpython-dev/vOhFapVJneU
            try:
                from ctypes import OleDLL

                # Turn on high-DPI awareness to make sure rendering is sharp on big
                # monitors with font scaling enabled.
                OleDLL('shcore').SetProcessDpiAwareness(1)
            except AttributeError:
                # We're on a non-Windows box.
                pass
            except OSError:
                # exc.winerror is often E_ACCESSDENIED (-2147024891/0x80070005).
                # This occurs after the first run, when the parameter is reset in the
                # executable's manifest and then subsequent calls raise this exception
                # See last paragraph of Remarks at
                # https://msdn.microsoft.com/en-us/library/dn302122(v=vs.85).aspx
                pass
        # try:
        MainWindow.PrintSysInfo()
        MainWindow().MainLoop()
# except BaseException as err:
#     print(err)
