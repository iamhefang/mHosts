# -*- coding: utf-8 -*-
import sys
from threading import Timer

from wx import Frame, DEFAULT_FRAME_STYLE, SYSTEM_MENU, TAB_TRAVERSAL, MenuBar, Menu, MenuItem, ITEM_NORMAL, StatusBar, \
    STB_SIZEGRIP, Font, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, \
    EmptyString, HORIZONTAL, TreeCtrl, Point, TR_DEFAULT_STYLE, EVT_MENU, Dialog, ID_ANY, DefaultPosition, \
    DEFAULT_DIALOG_STYLE, \
    Size, DefaultSize, Icon, BITMAP_TYPE_ICO, BoxSizer, VERTICAL, EXPAND, BOTH, FLEX_GROWMODE_SPECIFIED, FlexGridSizer, \
    RadioButton, StaticText, TextCtrl, Button, ALL, EVT_RADIOBUTTON, EVT_BUTTON, MessageBox, ICON_WARNING, \
    ComboBox, \
    ImageList, EVT_CLOSE, FONTWEIGHT_BOLD, Colour, SIMPLE_BORDER, \
    TRANSPARENT_WINDOW, DisplaySize, STAY_ON_TOP, FRAME_NO_TASKBAR, FRAME_FLOAT_ON_PARENT

from src.helpers import iconPath, GetIcons, Now
from src.settings import Settings, hostsDict
from src.views.AboutView import AboutView
from src.views.CodeView import CodeView


class MainFrame(Frame):

    def __init__(self, parent, dpi=(1, 1)):
        Frame.__init__(
            self, parent, id=ID_ANY, title=u" mHosts - v" + Settings.version(),
            pos=DefaultPosition,
            size=Size(700 * dpi[0], 500 * dpi[1]),
            style=DEFAULT_FRAME_STYLE | SYSTEM_MENU | TAB_TRAVERSAL
        )
        self.SetIcon(Icon(iconPath, BITMAP_TYPE_ICO))
        self.SetSizeHints(Size(500 * dpi[0], 350 * dpi[1]))
        self.menuBar = MenuBar(0)
        self.menuFile = Menu()
        self.menuItemNew = MenuItem(
            self.menuFile, ID_ANY, u"新建(&N)", EmptyString, ITEM_NORMAL)
        self.menuItemImport = MenuItem(
            self.menuFile, ID_ANY, u"导入(&I)", EmptyString, ITEM_NORMAL)
        if sys.platform != "linux":
            self.menuItemImport.Enable(False)
        self.menuFile.Append(self.menuItemNew)
        self.menuFile.Append(self.menuItemImport)

        self.menuFile.AppendSeparator()

        self.menuItemExit = MenuItem(
            self.menuFile, ID_ANY, u"退出(&Q)", EmptyString, ITEM_NORMAL)
        self.menuFile.Append(self.menuItemExit)

        self.menuBar.Append(self.menuFile, u"文件(&F)")

        self.menuHelp = Menu()

        self.menuItemSettings = MenuItem(
            self.menuHelp, ID_ANY, u"首选项(&P)", EmptyString, ITEM_NORMAL)
        if sys.platform != "linux":
            self.menuItemSettings.Enable(False)
        self.menuHelp.Append(self.menuItemSettings)

        self.menuItemHelpDoc = MenuItem(
            self.menuHelp, ID_ANY, u"帮助文档(&D)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemHelpDoc)

        self.menuItemCheckUpdate = MenuItem(
            self.menuHelp, ID_ANY, u"检查更新(&U)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemCheckUpdate)

        self.menuItemAbout = MenuItem(
            self.menuHelp, ID_ANY, u"关于(&A)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemAbout)

        self.menuBar.Append(self.menuHelp, u"帮助(&H)")

        self.SetMenuBar(self.menuBar)

        self.statusBar = StatusBar(self, ID_ANY, STB_SIZEGRIP)
        statusBarFont = Font(
            10, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, False, EmptyString)
        self.statusBar.SetFont(statusBarFont)
        self.SetStatusBar(self.statusBar)

        bSizer1 = BoxSizer(HORIZONTAL)

        self.images = {}

        self.imageList = ImageList(width=12, height=12)
        iconList = GetIcons().items()
        for name, bitmap in iconList:
            self.images[name] = self.imageList.Add(bitmap)

        self.hostsTree = TreeCtrl(
            self, ID_ANY,
            Point(0, 0),
            Size(180 * dpi[0], -1),
            TR_DEFAULT_STYLE
        )
        self.hostsTree.SetImageList(self.imageList)
        bSizer1.Add(self.hostsTree, 0, EXPAND, 5)

        # self.hostsListView = CheckListBox(self, size=Size(size[0] / 9, -1))
        # bSizer1.Add(self.hostsListView, 0, EXPAND, 5)

        # WARNING: wxPython code generation isn't supported for this widget yet.
        self.codeEditor = CodeView(self, dpi)
        bSizer1.Add(self.codeEditor, 1, EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(BOTH)

        # Connect Events
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemNew.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemExit.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemAbout.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemHelpDoc.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemSettings.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemImport.GetId())
        self.Bind(EVT_MENU, self.OnMenuClicked, id=self.menuItemCheckUpdate.GetId())

    def __del__(self):
        pass

    def Destroy(self):
        self.imageList.Destroy()
        Frame.Destroy(self)

    # Virtual event handlers, overide them in your derived class
    def OnMenuClicked(self, event):
        event.Skip()


class AboutDialog(Dialog):

    def __init__(self, parent, dpi=(1, 1)):
        Dialog.__init__(
            self, parent,
            id=ID_ANY,
            title=u" 关于 mHosts - v%s" % Settings.version(),
            pos=DefaultPosition,
            style=DEFAULT_DIALOG_STYLE | FRAME_FLOAT_ON_PARENT,
            size=Size(400 * dpi[0], 300 * dpi[1])
        )
        self.SetSizeHints(DefaultSize, DefaultSize)
        self.SetIcon(Icon(iconPath, BITMAP_TYPE_ICO))
        bSizer2 = BoxSizer(VERTICAL)

        self.aboutDialog = AboutView(self, self.GetSize())
        bSizer2.Add(self.aboutDialog, 0, EXPAND, 0)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(BOTH)

    def __del__(self):
        pass


class EditDialog(Dialog):
    __hosts = None
    __window = None

    def __init__(self, parent, dpi=(1, 1)):
        Dialog.__init__(
            self, parent,
            id=ID_ANY,
            title=u"编辑/添加Hosts",
            pos=Point(600, 600),
            size=Size(394 * dpi[0], 210 * dpi[1]),
            style=DEFAULT_DIALOG_STYLE | FRAME_FLOAT_ON_PARENT
        )
        self.__window = parent
        self.SetSizeHints(DefaultSize, DefaultSize)

        font = Font(10, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL,
                    FONTWEIGHT_NORMAL, False, EmptyString)
        inputSize = Size(260 * dpi[0], -1)
        self.SetFont(font)
        fgSizer3 = FlexGridSizer(0, 2, 0, 0)
        fgSizer3.SetFlexibleDirection(BOTH)
        fgSizer3.SetNonFlexibleGrowMode(FLEX_GROWMODE_SPECIFIED)

        self.localRadio = RadioButton(
            self, ID_ANY, u"本地Hosts", DefaultPosition, DefaultSize, 0)
        self.localRadio.SetFont(font)
        fgSizer3.Add(self.localRadio, 0, ALL, 5)
        self.localRadio.Bind(EVT_RADIOBUTTON, self.OnRadioChange)

        self.onlineRadio = RadioButton(
            self, ID_ANY, u"在线Hosts", DefaultPosition, DefaultSize, 0)
        fgSizer3.Add(self.onlineRadio, 0, ALL, 5)
        self.onlineRadio.Bind(EVT_RADIOBUTTON, self.OnRadioChange)

        self.m_staticText4 = StaticText(
            self, ID_ANY, u"名称", DefaultPosition, DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        fgSizer3.Add(self.m_staticText4, 0, ALL, 5)

        self.nameInput = TextCtrl(
            self, ID_ANY, EmptyString, DefaultPosition, inputSize, 0)
        fgSizer3.Add(self.nameInput, 0, ALL, 5)

        self.m_staticText5 = StaticText(
            self, ID_ANY, u"地址", DefaultPosition, DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        fgSizer3.Add(self.m_staticText5, 0, ALL, 5)

        self.urlInput = TextCtrl(
            self, ID_ANY, u"http://", DefaultPosition, inputSize, 0)
        fgSizer3.Add(self.urlInput, 0, ALL, 5)

        self.m_staticText3 = StaticText(
            self, ID_ANY, u"图标", DefaultPosition, DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        fgSizer3.Add(self.m_staticText3, 0, ALL, 5)

        self.iconComboBox = ComboBox(
            self, ID_ANY, u"请选择图标", DefaultPosition, inputSize, list(GetIcons().keys()), 0)
        self.iconComboBox.SetFont(font)
        fgSizer3.Add(self.iconComboBox, 0, ALL, 5)

        self.cancelButton = Button(
            self, ID_ANY, u"取消", DefaultPosition, DefaultSize, 0)
        fgSizer3.Add(self.cancelButton, 0, ALL, 5)

        self.saveButton = Button(
            self, ID_ANY, u"保存", DefaultPosition, DefaultSize, 0)
        fgSizer3.Add(self.saveButton, 0, ALL, 5)

        self.SetSizer(fgSizer3)
        self.Layout()

        self.Centre(BOTH)

        self.cancelButton.Bind(EVT_BUTTON, self.OnButtonClicked)
        self.saveButton.Bind(EVT_BUTTON, self.OnButtonClicked)
        self.Bind(EVT_CLOSE, self.OnClose)

    def __del__(self):
        pass

    def OnClose(self, event):
        self.SetHosts(None)
        event.Skip()

    def SetHosts(self, hosts):
        self.__hosts = hosts
        if hosts:
            if hosts["url"] and len(hosts["url"] > 0):
                self.onlineRadio.SetValue(hosts["url"])
            self.localRadio.SetValue(not hosts["url"])
            self.nameInput.SetValue(hosts["name"])
            self.urlInput.SetValue(hosts["url"] or "")
            self.iconComboBox.SetValue(hosts["icon"])
            self.onlineRadio.Enable(False)
            self.localRadio.Enable(False)
        else:
            self.onlineRadio.Enable(False)
            self.localRadio.Enable(True)
            self.localRadio.SetValue(True)
            self.urlInput.SetValue("")
            self.iconComboBox.SetValue("")
            self.nameInput.SetValue("")

    def OnButtonClicked(self, event):
        if event.GetId() == self.cancelButton.GetId():
            self.Close()
            return
        name = self.nameInput.GetValue()
        url = self.urlInput.GetValue()
        isOnline = self.onlineRadio.GetValue()
        if not isOnline:
            url = None
        if not name or len(name) < 1:
            MessageBox("请输入Hosts名称", "提示", ICON_WARNING)
        elif isOnline and (not url or len(url) < 1):
            MessageBox("请输入在线Hosts地址", "提示", ICON_WARNING)
        else:
            if self.__hosts:
                self.__hosts["name"] = name
                self.__hosts["url"] = url
                self.__hosts["lastUpdateTime"] = Now()
                self.__hosts["icon"] = self.iconComboBox.GetValue()
                hostsId = self.__hosts['id']
            else:
                hostsId = 0x1994 + len(Settings.settings["hosts"])
                Settings.settings["hosts"].append(hostsDict(
                    hostsId,
                    name,
                    url=url,
                    lastUpdateTime=Now(),
                    content="# Created by mHosts v%s, %s\n" % (Settings.version(), Now()),
                    icon=self.iconComboBox.GetValue()
                ))
            Settings.Save()
            self.__window.InitHostsTree(select=hostsId)
            self.Close()

    def OnRadioChange(self, event):
        self.urlInput.Enable(event.GetId() == self.onlineRadio.GetId())


class MessagePanel(Frame):

    def __init__(self, dpi=(1, 1)):
        width = 300 * dpi[0]
        height = 80 * dpi[1]
        screenSize = DisplaySize()
        x = screenSize[0] - width - 10 * dpi[0],
        y = screenSize[1] - height - 100 * dpi[1]
        Frame.__init__(
            self,
            parent=None,
            id=ID_ANY,
            pos=Point(x[0], y),
            size=Size(width, height),
            style=SIMPLE_BORDER | TRANSPARENT_WINDOW | STAY_ON_TOP | FRAME_NO_TASKBAR,
            name=EmptyString
        )

        bSizer4 = BoxSizer(VERTICAL)

        self.msgTitle = StaticText(self, ID_ANY, u"MyLabel", DefaultPosition, DefaultSize, 0)
        self.msgTitle.Wrap(-1)

        self.msgTitle.SetFont(Font(13, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD, False, EmptyString))

        bSizer4.Add(self.msgTitle, 0, ALL, 5)

        self.msgContent = StaticText(self, ID_ANY, u"MyLabel", DefaultPosition, DefaultSize, 0)
        self.msgContent.Wrap(-1)

        self.msgContent.SetFont(
            Font(12, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, False, EmptyString))

        bSizer4.Add(self.msgContent, 0, EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()
        # colorWhite = Colour(255, 255, 255)
        self.SetBackgroundColour(Colour(240, 240, 240))
        # self.msgTitle.SetForegroundColour(colorWhite)
        # self.msgContent.SetForegroundColour(colorWhite)

    def __del__(self):
        pass

    @staticmethod
    def Send(message: str, title: str, dpi=(1, 1), delay=3):
        dialog = MessagePanel(dpi)
        dialog.msgTitle.SetLabelText(title)
        dialog.msgContent.SetLabelText(" " + message.replace("\n", "\n "))
        dialog.Show()
        if delay > 0:
            Timer(delay, dialog.CloseNotify).start()

    def CloseNotify(self):
        self.Close()
