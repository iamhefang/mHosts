# _*_ coding: utf-8 _*_

from wx import App, BITMAP_TYPE_ICO, Icon, EVT_MENU, EVT_CLOSE, adv

from widgets import MainWindow, AboutDialog


class Application(App):
    def __init__(self):
        App.__init__(self)
        self.window = MainWindow(None)
        self.aboutDialog = AboutDialog(self.window)
        self.window.SetIcon(Icon("icons/logo.ico", BITMAP_TYPE_ICO))

        adv.TaskBarIcon().SetIcon(Icon("icons/logo.ico", BITMAP_TYPE_ICO))

        self.window.Show()
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.window.menuItemExit.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.window.menuItemAbout.GetId())
        self.window.Bind(EVT_CLOSE, self.OnWindowClose, id=self.window.GetId())

    def OnWindowClose(self, event):
        self.window.Show(False)

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnMenuClicked(self, event):
        if event.GetId() == self.window.menuItemExit.GetId():
            exit(0)
        elif event.GetId() == self.window.menuItemAbout.GetId():
            self.ShowAboutDialog()


if __name__ == '__main__':
    app = Application()
    app.MainLoop()
