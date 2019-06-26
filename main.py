# _*_ coding: utf-8 _*_

import wx

from windows import MainWindow

app = wx.App()

window = MainWindow(None)

window.Show()

app.MainLoop()
