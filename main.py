# _*_ coding: utf-8 _*_

import wx

from widgets import MainWindow, AboutDialog


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
        self.window.Bind(wx.EVT_CLOSE, self.OnWindowClose, id=self.window.GetId())

    def OnWindowClose(self, event):
        self.window.Show(False)

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnMenuClicked(self, event):
        if event.GetId() == self.window.menuItemExit.GetId():
            exit(0)
        elif event.GetId() == self.window.menuItemAbout.GetId():
            self.ShowAboutDialog()


app = Application()
app.MainLoop()
