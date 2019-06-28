# _*_ coding: utf-8 _*_

from wx import App, BITMAP_TYPE_ICO, Icon, EVT_MENU, EVT_CLOSE, adv

from helpers import fetchCurrentVersion
from widgets import MainWindow, AboutDialog


class Application(App):
    def __init__(self):
        App.__init__(self)
        self.window = MainWindow(None)
        self.trayIcon = adv.TaskBarIcon()
        self.aboutDialog = AboutDialog(self.window)

        self.window.SetTitle(u"mHosts - " + fetchCurrentVersion())
        self.window.SetIcon(Icon("icons/logo.ico", BITMAP_TYPE_ICO))
        self.window.Show()
        self.aboutDialog.SetTitle(u"关于 mHosts - " + fetchCurrentVersion())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.window.menuItemExit.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.window.menuItemAbout.GetId())
        self.window.Bind(EVT_CLOSE, self.OnWindowClose, id=self.window.GetId())
        self.InitTrayIcon()

    def InitTrayIcon(self):
        self.trayIcon.SetIcon(Icon("icons/logo.ico", BITMAP_TYPE_ICO))
        self.trayIcon.Bind(adv.EVT_TASKBAR_LEFT_DCLICK, self.ShowMainWindow)

    def ShowMainWindow(self, event):
        self.window.Show(not self.window.IsShown())

    def OnWindowClose(self, event):
        self.window.Show(False)

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnMenuClicked(self, event):
        if event.GetId() == self.window.menuItemExit.GetId():
            self.Exit()
        elif event.GetId() == self.window.menuItemAbout.GetId():
            self.ShowAboutDialog()

    def Exit(self):
        self.trayIcon.Destroy()
        self.ExitMainLoop()
        exit(0)


if __name__ == '__main__':
    app = Application()
    app.MainLoop()
