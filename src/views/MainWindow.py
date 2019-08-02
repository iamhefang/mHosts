import os
import sys
from subprocess import Popen

from wx import App, MessageBox, ICON_ERROR, EVT_CLOSE, LaunchDefaultBrowser, DisplaySize, \
    EVT_TREE_SEL_CHANGED, EVT_TREE_ITEM_RIGHT_CLICK, Menu, EVT_MENU, CommandEvent, Colour, EVT_TREE_ITEM_ACTIVATED, \
    Locale, LANGUAGE_CHINESE_SIMPLIFIED
from wx.stc import EVT_STC_CHANGE

from src import Hosts
from src.BackgroundThread import BackgroundThread
from src.CheckNewVersionThread import CheckNewVersionThread
from src.helpers import NowToTimestamp, Now, ParseHosts
from src.settings import Settings, systemHosts, ID_SYSTEM_HOSTS
from src.views.TrayIcon import TrayIcon
from src.widgets import MainFrame, AboutDialog, EditDialog, MessagePanel


class MainWindow(MainFrame):
    app = App()
    size = DisplaySize()
    dpiX = 1
    dpiY = 1
    __currentSelectHost = None
    __currentEditHost = None

    def __init__(self):
        self.app.locale = Locale(LANGUAGE_CHINESE_SIMPLIFIED)
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
        selectId = self.hostsTree.AppendItem(
            root, "当前系统", image=self.images[sys.platform], data=systemHosts
        )
        for hosts in Settings.settings["hosts"]:
            itemId = self.hostsTree.AppendItem(
                root, hosts["name"], data=hosts, image=self.images[hosts["icon"]]
            )
            self.hostsTree.SetItemBold(itemId, hosts["active"])
            if hosts["active"]:
                self.hostsTree.SetItemTextColour(
                    itemId, Colour(0x12, 0x96, 0xdb)
                )
            if hosts["id"] == select:
                selectId = itemId
        self.hostsTree.ExpandAll()

        if selectId:
            self.hostsTree.SelectItem(selectId)

    def OnHostsTreeActivated(self, event):
        itemId = event.GetItem()
        hosts = self.hostsTree.GetItemData(itemId)
        if hosts["id"] == ID_SYSTEM_HOSTS or hosts['alwaysApply']:
            return
        self.ApplyHosts(hosts["id"])

    def InitMainWindow(self):
        self.Show()
        self.codeEditor.SetValue(Hosts.GetSystemHosts())
        self.codeEditor.SetReadOnly(True)
        self.Bind(EVT_CLOSE, self.OnWindowClose)
        self.statusBar.SetFieldsCount(3)
        self.SetStatusWidths([-1, -2, -1])
        self.statusBar.SetStatusText(
            "当前共%d个Hosts规则" % len(Settings.settings["hosts"]), 0
        )
        self.statusBar.SetStatusText("编辑自动保存, 双击应用到系统", 1)
        self.hostsTree.Bind(EVT_TREE_SEL_CHANGED, self.OnHostsTreeItemSelect)
        self.hostsTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.ShowTreeItemMenu)
        self.hostsTree.Bind(EVT_TREE_ITEM_ACTIVATED, self.OnHostsTreeActivated)
        self.codeEditor.Bind(EVT_STC_CHANGE, self.OnKeyUp)
        updateTime = Settings.settings["lastCheckUpdateTime"]
        if updateTime and NowToTimestamp(updateTime) < 0:
            self.CheckUpdate()

    def OnKeyUp(self, event):
        # 如果是只读状态, 则忽略按键事件
        if self.codeEditor.GetReadOnly() or not self.__currentEditHost:
            return
        self.__currentEditHost["content"] = self.codeEditor.GetValue()
        # 保存

    def ShowTreeItemMenu(self, event):
        hosts = self.hostsTree.GetItemData(event.GetItem())
        if not hosts:
            return
        self.__currentSelectHost = hosts
        menu = Menu()
        popMenuActive = menu.Append(TrayIcon.ID_TREE_MENU_SET_ACTIVE, "设置为当前Hosts")
        if hosts["id"] == ID_SYSTEM_HOSTS or hosts['alwaysApply']:
            popMenuActive.Enable(False)
        else:
            popMenuActive.Enable(not hosts["active"])
        menu.AppendSeparator()

        popMenuEdit = menu.Append(TrayIcon.ID_TREE_MENU_EDIT, "编辑")
        popMenuEdit.Enable(hosts["id"] != ID_SYSTEM_HOSTS)

        popMenuDelete = menu.Append(TrayIcon.ID_TREE_MENU_DELETE, "删除")
        popMenuDelete.Enable(hosts["id"] != ID_SYSTEM_HOSTS)

        # menu.Append(TrayIcon.ID_TREE_MENU_REFRESH, "刷新")

        self.hostsTree.PopupMenu(menu, event.GetPoint())
        self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked)
        # self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked, popMenuDelete.GetId())
        # self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked, popMenuActive.GetId())
        # self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked, popMenuEdit.GetId())
        # self.hostsTree.Bind(EVT_MENU, self.OnMenuClicked, popMenuRefresh.GetId())

    def OnHostsTreeItemSelect(self, event):
        hosts = self.hostsTree.GetItemData(event.GetItem())
        if not hosts:
            return
        self.codeEditor.SetReadOnly(False)
        self.codeEditor.SetValue(Hosts.GetSystemHosts() if hosts["id"] == ID_SYSTEM_HOSTS else hosts["content"])
        self.codeEditor.SetReadOnly(hosts["readOnly"])
        self.codeEditor.SetHosts(hosts)

    def ToggleWindow(self):
        self.Iconize(not self.IsIconized())
        self.Show(not self.IsShown())
        if self.IsShown():
            self.Raise()

    def OnWindowClose(self, event):
        self.Iconize(True)
        self.Hide()
        return False

    def ShowAboutDialog(self):
        self.aboutDialog.Show(True)

    def OnTaskBarHostsMenuClicked(self, event):
        self.ApplyHosts(event.GetId())
        pass

    def ApplyHosts(self, hostsId: int):
        commonHostsLines = "# hosts file apply by mHosts v%s, %s\n " % (Settings.version(), Now())
        currentHostsLines = ""
        currentHosts = None

        for hosts in Settings.settings["hosts"]:
            if hosts["id"] == hostsId:
                currentHostsLines += "# ---------------- %(name)s ----------------%(br)s%(content)s%(br)s" % {
                    "name": hosts['name'],
                    "br": os.linesep,
                    "content": hosts['content']
                }
                currentHosts = hosts
            if hosts["alwaysApply"]:
                commonHostsLines += "# ---------------- %(name)s ----------------%(br)s%(content)s%(br)s" % {
                    "name": hosts['name'],
                    "br": os.linesep,
                    "content": hosts['content']
                }

        hostsToApply = commonHostsLines + os.linesep + currentHostsLines
        try:
            if Hosts.Save2System(ParseHosts(hostsToApply)):
                for hosts in Settings.settings["hosts"]:
                    hosts["active"] = hosts["id"] == hostsId
                refreshDnsRes = Hosts.TryFlushDNSCache()
                MessagePanel.Send(
                    "Hosts已设置为" + currentHosts["name"] + "\nDNS缓存刷新" + ("成功" if refreshDnsRes else "失败"),
                    "保存成功",
                    dpi=(self.dpiX, self.dpiY)
                )
            else:
                MessageBox("保存失败", "提示", ICON_ERROR)
            self.InitHostsTree(ID_SYSTEM_HOSTS)
            Settings.Save()
        except Exception as e:
            message = str(e)
            if "Permission denied" in message:
                MessageBox("尝试写入hosts时权限不足, 保存失败, 请以管理员身份运行该软件", "权限不足", ICON_ERROR)
            else:
                MessageBox(message, "保存时出错", ICON_ERROR)

    def ShowEditDialog(self, hosts):
        self.editDialog.Show()
        self.editDialog.SetHosts(hosts)

    def OnMenuClicked(self, event: CommandEvent):
        handlers = {
            self.menuItemExit.GetId(): self.Exit,
            self.menuItemAbout.GetId(): self.ShowAboutDialog,
            self.menuItemHelpDoc.GetId(): lambda: LaunchDefaultBrowser("https://hefang.link/url/mhosts-doc"),
            self.menuItemNew.GetId(): lambda: self.ShowEditDialog(None),
            self.menuItemCheckUpdate.GetId(): self.CheckUpdate,
            TrayIcon.ID_EXIT: self.Exit,
            TrayIcon.ID_TOGGLE: self.ToggleWindow,
            TrayIcon.ID_REFRESH_DNS: MainWindow.DoRefreshDNS,
            TrayIcon.ID_NEW: lambda: self.ShowEditDialog(None),
            TrayIcon.ID_ABOUT: lambda: self.aboutDialog.Show(),
            TrayIcon.ID_IMPORT: None,
            TrayIcon.ID_LUNCH_CHROME: lambda: MainWindow.LunchChrome(),
            TrayIcon.ID_LUNCH_CHROME_CROS: lambda: MainWindow.LunchChrome(
                "--disable-web-security --user-data-dir"
            ),
            TrayIcon.ID_LUNCH_CHROME_NO_PLUGINS: lambda: MainWindow.LunchChrome(
                "--disable-plugins --disable-extensions"
            ),
            TrayIcon.ID_TREE_MENU_EDIT: lambda: self.ShowEditDialog(self.__currentSelectHost),
            TrayIcon.ID_TREE_MENU_SET_ACTIVE: lambda: self.ApplyHosts(
                self.__currentSelectHost["id"]
            ),
            TrayIcon.ID_TREE_MENU_DELETE: lambda: self.DeleteHosts(self.__currentSelectHost)
        }
        if event.GetId() in handlers:
            callback = handlers[event.GetId()]
            if callable(callback):
                callback()
            else:
                MessagePanel.Send("该菜单绑定的事件不可用", "菜单点击",
                                  dpi=(self.dpiX, self.dpiY))
        else:
            MessagePanel.Send("该菜单没有绑定事件", "菜单点击", dpi=(self.dpiX, self.dpiY))

    def CheckUpdate(self):
        CheckNewVersionThread(self).start()

    def DeleteHosts(self, hosts: dict):
        if hosts['active']:
            MessageBox("无法删除当前应用的hosts", "删除失败", ICON_ERROR)
            return
        for index, host in enumerate(Settings.settings["hosts"]):
            if host["id"] == hosts["id"]:
                del Settings.settings["hosts"][index]
                MessagePanel.Send("Hosts'%(name)s'已删除" % hosts, "删除成功", dpi=(self.dpiX, self.dpiY))
                break
        self.InitHostsTree()

    @staticmethod
    def LunchChrome(args=""):
        chromePath = Settings.settings["chromePath"]
        if os.path.exists(chromePath):
            if ' ' in chromePath:
                chromePath = '"%s"' % chromePath
            cmd = u'%s %s' % (chromePath, args)
            Popen(cmd)
        else:
            Settings.settings["chromePath"] = ""
            MessageBox("当前配置的Chrome路径'%s'不存在" % chromePath if chromePath else "当前未配置Chrome路径", "启动失败", ICON_ERROR)

    @staticmethod
    def DoRefreshDNS():
        Hosts.TryFlushDNSCache()
        MessagePanel.Send(u"刷新DNS成功", u"提示")

    def Exit(self):
        BackgroundThread.stopAllBackThread()
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
