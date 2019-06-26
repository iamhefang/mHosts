# _*_ coding: utf-8 _*_

import wx

from widgets.AboutDialog import AboutDialog
from widgets.MainWindow import MainWindow


class Application(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        self.window = MainWindow(None)
        self.aboutDialog = AboutDialog(self.window)
        # trayIcon = wx.EmptyIcon()
        # trayIcon.LoadFile("")
        self.window.Show()
        self.Bind(wx.EVT_MENU, self.OnMenuClicked, id=self.window.menuItemExit.GetId())
        self.Bind(wx.EVT_MENU, self.OnMenuClicked, id=self.window.menuItemAbout.GetId())

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnMenuClicked(self, event):
        print(event.GetId())
        if event.GetId() == self.window.menuItemExit.GetId():
            exit(0)
        elif event.GetId() == self.window.menuItemAbout.GetId():
            self.ShowAboutDialog()


app = Application()
app.MainLoop()
