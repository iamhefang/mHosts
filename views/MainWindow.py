import os
import sys

from wx import App, MessageBox, ICON_ERROR, OK, ICON_NONE, EVT_CLOSE, LaunchDefaultBrowser, DisplaySize, \
    EVT_TREE_SEL_CHANGED, EVT_TREE_ITEM_RIGHT_CLICK, Menu, EVT_MENU, CommandEvent

import Hosts
from CheckNewVersionThread import CheckNewVersionThread
from helpers import NowToTimestamp
from settings import Settings, systemHosts, ID_SYSTEM_HOSTS
from views.TrayIcon import TrayIcon
from widgets import MainFrame, AboutDialog, EditDialog


class MainWindow(MainFrame):
    app = App()
    size = DisplaySize()
    dpiX = 1
    dpiY = 1
    __currentHost = None

    def __init__(self):
        realSize = DisplaySize()
        self.dpiX = realSize[0] / self.size[0]
        self.dpiY = realSize[1] / self.size[1]
        MainFrame.__init__(self, None, dpi=(self.dpiY, self.dpiY))
        self.trayIcon = TrayIcon(self)
        self.aboutDialog = AboutDialog(self, dpi=(self.dpiY, self.dpiY))
        self.editDialog = EditDialog(self, dpi=(self.dpiY, self.dpiY))

        self.InitMainWindow()
        self.InitHostsTree(ID_SYSTEM_HOSTS)

    def InitHostsTree(self, select=None):
        self.hostsTree.DeleteAllItems()
        root = self.hostsTree.AddRoot("全部Hosts", image=self.images["logo"])
        selectId = self.hostsTree.AppendItem(root, "当前系统", image=self.images[sys.platform], data=systemHosts)

        for hosts in Settings.settings["hosts"]:
            itemId = self.hostsTree.AppendItem(root, hosts["name"], data=hosts, image=self.images[hosts["icon"]])
            if hosts["id"] == select:
                selectId = itemId
        self.hostsTree.ExpandAll()

        if selectId:
            self.hostsTree.SelectItem(selectId)

    def InitMainWindow(self):
        self.Show()
        self.codeEditor.SetValue(Hosts.GetSystemHosts())
        self.codeEditor.SetReadOnly(True)
        self.Bind(EVT_CLOSE, self.OnWindowClose)
        self.statusBar.SetFieldsCount(3)
        self.SetStatusWidths([-1, -2, -1])
        self.statusBar.SetStatusText("当前共%d个Hosts规则" % len(Settings.settings["hosts"]), 0)
        self.hostsTree.Bind(EVT_TREE_SEL_CHANGED, self.OnHostsTreeItemSelect)
        self.hostsTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.ShowTreeItemMenu)
        updateTime = Settings.settings["lastCheckUpdateTime"]
        if updateTime and NowToTimestamp(updateTime) < 0:
            self.CheckUpdate()

    def ShowTreeItemMenu(self, event):
        hosts = self.hostsTree.GetItemData(event.GetItem())
        if not hosts:
            return
        self.__currentHost = hosts
        menu = Menu()
        print(not hosts["active"] or not hosts["alwaysApply"] or hosts["id"] != ID_SYSTEM_HOSTS)
        setToCurrent = menu.Append(TrayIcon.ID_TREE_MENU_SET_ACTIVE, "设置为当前Hosts")
        if hosts["id"] == ID_SYSTEM_HOSTS or hosts['alwaysApply']:
            setToCurrent.Enable(False)
        else:
            setToCurrent.Enable(not hosts["active"])
        menu.AppendSeparator()
        menu.Append(TrayIcon.ID_TREE_MENU_EDIT, "编辑").Enable(hosts["id"] != ID_SYSTEM_HOSTS)
        menu.Append(TrayIcon.ID_TREE_MENU_DELETE, "删除").Enable(hosts["id"] != ID_SYSTEM_HOSTS)
        menu.Append(TrayIcon.ID_TREE_MENU_REFRESH, "刷新")
        self.hostsTree.PopupMenu(menu, event.GetPoint())
        self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked)

    def ShowHostsInEditor(self, event):
        pass

    def OnHostsTreeItemSelect(self, event):
        hosts = self.hostsTree.GetItemData(event.GetItem())
        if not hosts:
            return
        self.codeEditor.SetValue(Hosts.GetSystemHosts() if hosts["id"] == ID_SYSTEM_HOSTS else hosts["content"])
        self.codeEditor.SetReadOnly(hosts["readOnly"])

    def OnCodeEditorKeyUp(self, event):
        if event.cmdDown and event.KeyCode == 83:
            pass

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

    def OnTaskBarHostsMenuClicked(self, event):
        commonHostsContent = ""
        currentHostsContent = ""
        currentHosts = None

        for hosts in Settings.settings["hosts"]:
            if hosts["id"] == event.GetId():
                currentHostsContent = hosts["content"]
                currentHosts = hosts
            if hosts["alwaysApply"]:
                commonHostsContent += hosts["content"]
            else:
                hosts["active"] = hosts["id"] == event.GetId()

        if Hosts.Save2System(commonHostsContent + "\n" + currentHostsContent):
            Hosts.TryFlushDNSCache()
            MessageBox("Hosts已设置为" + currentHosts["name"], "保存成功", ICON_NONE)
        else:
            MessageBox("保存失败", "提示", ICON_ERROR)

    def ShowEditDialog(self):
        self.editDialog.Show()
        self.editDialog.SetHosts(self.__currentHost)
        pass

    def OnMenuClicked(self, event: CommandEvent):
        handlers = {
            self.menuItemExit.GetId(): self.Exit,
            self.menuItemAbout.GetId(): self.ShowAboutDialog,
            self.menuItemHelpDoc.GetId(): lambda: LaunchDefaultBrowser("https://hefang.link/url/mhosts-doc"),
            self.menuItemNew.GetId(): self.ShowEditDialog,
            self.menuItemCheckUpdate.GetId(): self.CheckUpdate,
            TrayIcon.ID_EXIT: self.Exit,
            TrayIcon.ID_TOGGLE: self.ToggleWindow,
            TrayIcon.ID_REFRESH_DNS: MainWindow.DoRefreshDNS,
            TrayIcon.ID_NEW: self.ShowEditDialog,
            TrayIcon.ID_IMPORT: None,
            TrayIcon.ID_LUNCH_CHROME: lambda: MainWindow.LunchChrome(),
            TrayIcon.ID_LUNCH_CHROME_CROS: lambda: MainWindow.LunchChrome(
                "--disable-web-security --user-data-dir"
            ),
            TrayIcon.ID_LUNCH_CHROME_NO_PLUGINS: lambda: MainWindow.LunchChrome(
                "--disable-plugins --disable-extensions"
            ),
            TrayIcon.ID_TREE_MENU_EDIT: lambda: self.ShowEditDialog()
        }
        if event.GetId() in handlers:
            callback = handlers[event.GetId()]
            if callable(callback):
                callback()
            else:
                print("该菜单绑定的事件不可用")
        else:
            print("该菜单没有绑定事件")

    def CheckUpdate(self):
        CheckNewVersionThread(self).start()

    @staticmethod
    def LunchChrome(args=""):
        chromePath = Settings.settings["chrome-path"]
        if chromePath:
            if ' ' in chromePath:
                chromePath = '"%s"' % chromePath
            cmd = u'%s %s' % (chromePath, args)
            print("当前Chrome命令为: " + cmd)
            os.system(cmd)

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
        Settings.Save()

    @staticmethod
    def PrintSysInfo():
        print("版本：", Settings.version())
        print("系统：", sys.platform)
        print("hosts:", Hosts.GetHostsPath())
