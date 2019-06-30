import os
import sys
import traceback

from wx import App, MessageBox, ICON_ERROR, OK, ICON_NONE, EVT_CLOSE, LaunchDefaultBrowser, EVT_TREE_ITEM_ACTIVATED

from Hosts import Hosts
from helpers import GetChromePath
from version import version
from views.TrayIcon import TrayIcon
from widgets import MainFrame, AboutDialog


class MainWindow(MainFrame):
    hostsList = [
        Hosts("当前系统", Hosts.GetHostsPath()),
        Hosts("Hosts 1", Hosts.GetHostsPath())
    ]
    app = App()

    def __init__(self):
        MainFrame.__init__(self, None)
        self.trayIcon = TrayIcon(self)
        self.aboutDialog = AboutDialog(self)
        self.InitMainWindow()
        root = self.hostsTree.AddRoot("全部Hosts")
        for hosts in self.hostsList:
            self.hostsTree.AppendItem(root, hosts.title)
        self.hostsTree.ExpandAll()

    def InitMainWindow(self):
        self.Show()
        self.codeEditor.SetText(Hosts.GetSystemHosts())
        self.Bind(EVT_CLOSE, self.OnWindowClose)
        self.statusBar.SetFieldsCount(2)
        self.SetStatusWidths([-1, -3])
        self.statusBar.SetStatusText("当前共%d个Hosts规则" % len(self.hostsList), 0)
        self.hostsTree.Bind(EVT_TREE_ITEM_ACTIVATED, self.OnHostTreeItemClicked)

    def OnHostTreeItemClicked(self, event):
        event.Skip()

    def OnCodeEditorKeyUp(self, event):
        if event.cmdDown and event.KeyCode == 83:
            try:
                with open(Hosts.GetHostsPath(), mode="w") as file:
                    if file.write(self.codeEditor.GetText()) > 0:
                        MessageBox(u"保存成功")
                    else:
                        MessageBox(u"保存失败")
            except PermissionError:
                MessageBox(r"没有修改%s的权限" % Hosts.GetHostsPath(), u"保存失败", OK | ICON_ERROR, self)
            except:
                MessageBox(traceback.format_exc(), u"保存失败", OK | ICON_ERROR, self)

    def ToggleWindow(self):
        self.Show(not self.IsShown())
        self.Iconize(not self.IsIconized())
        if self.IsShown():
            self.Raise()

    def OnWindowClose(self, event):
        self.Iconize(True)
        self.Hide()
        return False

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnHostsMenuClicked(self, event):
        for hosts in self.hostsList:
            hosts.SetActive(hosts.GetId() == event.GetId())

    def OnMenuClicked(self, event):
        handlers = {
            self.menuItemExit.GetId(): self.Exit,
            self.menuItemAbout.GetId(): self.ShowAboutDialog,
            self.menuItemHelpDoc.GetId(): lambda: LaunchDefaultBrowser("https://hefang.link/url/mhosts-doc"),
            TrayIcon.ID_EXIT: self.Exit,
            TrayIcon.ID_TOGGLE: self.ToggleWindow,
            TrayIcon.ID_REFRESH_DNS: MainWindow.DoRefreshDNS,
            TrayIcon.ID_NEW: None,
            TrayIcon.ID_IMPORT: None,
            TrayIcon.ID_LUNCH_CHROME: lambda: MainWindow.LunchChrome(),
            TrayIcon.ID_LUNCH_CHROME_CROS: lambda: MainWindow.LunchChrome("--disable-web-security --user-data-dir"),
            TrayIcon.ID_LUNCH_CHROME_NO_PLUGINS: lambda: MainWindow.LunchChrome(
                "--disable-plugins --disable-extensions"),
        }
        if event.GetId() in handlers:
            callback = handlers[event.GetId()]
            if callable(callback):
                callback()
            else:
                print("该菜单绑定的事件不可用")
        else:
            print("该菜单没有绑定事件")

    @staticmethod
    def LunchChrome(args=""):
        chromePath = GetChromePath()
        if chromePath:
            cmd = u'%s %s' % (chromePath, args)
            print("当前Chrome命令为: " + cmd)
            os.system(cmd)
        pass

    @staticmethod
    def DoRefreshDNS():
        Hosts.TryFlushDNSCache()
        MessageBox(u"刷新DNS成功", u"提示", OK | ICON_NONE)

    def Exit(self):
        self.trayIcon.Destroy()
        self.aboutDialog.Close()
        self.aboutDialog.Destroy()
        self.Close()
        self.Destroy()
        self.app.ExitMainLoop()

    def MainLoop(self):
        self.app.MainLoop()

    @staticmethod
    def PrintSysInfo():
        print("版本：", version)
        print("系统：", sys.platform)
        print("hosts:", Hosts.GetHostsPath())
