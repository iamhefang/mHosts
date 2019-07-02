from wx import MenuItem, Icon, BITMAP_TYPE_ICO, Menu, EVT_MENU, NewId, adv, ITEM_CHECK, ID_ANY
from wx.adv import TaskBarIcon

from helpers import iconPath
from settings import Settings


class TrayIcon(TaskBarIcon):
    ID_EXIT = NewId()
    ID_UPDATE = NewId()
    ID_TOGGLE = NewId()
    ID_REFRESH_DNS = NewId()
    # 新建Hosts
    ID_NEW = NewId()
    # 导入Hosts
    ID_IMPORT = NewId()
    # 启动Chrome
    ID_LUNCH_CHROME = NewId()
    # 允许跨域启动Chrome
    ID_LUNCH_CHROME_CROS = NewId()
    # 禁用插件
    ID_LUNCH_CHROME_NO_PLUGINS = NewId()

    __window = None
    menu = None

    def __init__(self, window):
        TaskBarIcon.__init__(self)
        self.__window = window
        self.SetIcon(Icon(iconPath, BITMAP_TYPE_ICO))
        self.Bind(adv.EVT_TASKBAR_LEFT_DCLICK, self.ToggleWindow)
        ids = [
            self.ID_IMPORT,
            self.ID_NEW,
            self.ID_REFRESH_DNS,
            self.ID_TOGGLE,
            self.ID_EXIT,
            self.ID_UPDATE,
            self.ID_LUNCH_CHROME,
            self.ID_LUNCH_CHROME_CROS,
            self.ID_LUNCH_CHROME_NO_PLUGINS
        ]
        for itemId in ids:
            self.Bind(EVT_MENU, window.OnMenuClicked, id=itemId)

    def CreatePopupMenu(self):
        menu = Menu()
        menu.Append(ID_ANY, "mHosts v" + Settings.version()).Enable(False)
        menu.Append(self.ID_TOGGLE, r"%s主窗口" % ("隐藏" if self.__window.IsShown() else "显示"))
        menu.AppendSeparator()
        for hosts in Settings.settings["hosts"]:
            item = MenuItem(menu, hosts["id"], hosts["name"], kind=ITEM_CHECK)
            item.Enable(not hosts['alwaysApply'])
            menu.Append(item)
            menu.Check(hosts["id"], hosts["active"] or hosts["alwaysApply"])
            self.Bind(EVT_MENU, self.__window.OnTaskBarHostsMenuClicked, id=hosts["id"])

        newHostMenu = Menu()
        newHostMenu.Append(self.ID_NEW, "新建")
        newHostMenu.Append(self.ID_IMPORT, "导入")
        menu.Append(-1, "新建Hosts方案", newHostMenu)

        menu.AppendSeparator()
        menu.Append(self.ID_REFRESH_DNS, u"刷新DNS缓存")
        if Settings.settings["chromePath"]:
            chromeMenu = Menu()
            chromeMenu.Append(self.ID_LUNCH_CHROME, "直接启动")
            chromeMenu.Append(self.ID_LUNCH_CHROME_CROS, "允许跨域请求")
            chromeMenu.Append(self.ID_LUNCH_CHROME_NO_PLUGINS, "禁用所有插件")
            menu.Append(-1, "启动 Google Chrome 浏览器", chromeMenu)

        menu.AppendSeparator()
        menu.Append(self.ID_UPDATE, "更新")
        menu.Append(self.ID_EXIT, "退出")
        self.menu = menu
        return menu

    def ToggleWindow(self, event):
        self.__window.ToggleWindow()
