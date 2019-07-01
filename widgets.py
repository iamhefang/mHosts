# -*- coding: utf-8 -*-

from wx import Frame, DEFAULT_FRAME_STYLE, SYSTEM_MENU, TAB_TRAVERSAL, MenuBar, Menu, MenuItem, ITEM_NORMAL, StatusBar, \
    STB_SIZEGRIP, Font, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, \
    EmptyString, HORIZONTAL, TreeCtrl, Point, TR_DEFAULT_STYLE, EVT_MENU, Dialog, ID_ANY, DefaultPosition, \
    DEFAULT_DIALOG_STYLE, \
    Size, DefaultSize, Icon, BITMAP_TYPE_ICO, BoxSizer, VERTICAL, EXPAND, BOTH, DisplaySize

from helpers import iconPath
from version import version
from views.CodeView import CodeView
from views.HtmlView import HtmlView


class MainFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, id=ID_ANY, title=u" mHosts - v" + version,
                       pos=DefaultPosition,
                       style=DEFAULT_FRAME_STYLE | SYSTEM_MENU | TAB_TRAVERSAL)
        size = DisplaySize()
        self.SetIcon(Icon(iconPath, BITMAP_TYPE_ICO))
        self.SetSize(Size(size[0] / 2, size[1] / 1.5))
        self.SetSizeHints(Size(size[0] / 3, size[1] / 2.5), DefaultSize)

        self.menuBar = MenuBar(0)
        self.menuFile = Menu()
        self.menuItemNew = MenuItem(self.menuFile, ID_ANY, u"新建(&N)", EmptyString, ITEM_NORMAL)
        self.menuItemImport = MenuItem(self.menuFile, ID_ANY, u"导入(&I)", EmptyString, ITEM_NORMAL)
        self.menuFile.Append(self.menuItemNew)
        self.menuFile.Append(self.menuItemImport)

        self.menuFile.AppendSeparator()

        self.menuItemExit = MenuItem(self.menuFile, ID_ANY, u"退出(&Q)", EmptyString, ITEM_NORMAL)
        self.menuFile.Append(self.menuItemExit)

        self.menuBar.Append(self.menuFile, u"文件(&F)")

        self.menuHelp = Menu()

        self.menuItemSettings = MenuItem(self.menuHelp, ID_ANY, u"首选项(&P)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemSettings)

        self.menuItemHelpDoc = MenuItem(self.menuHelp, ID_ANY, u"帮助文档(&D)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemHelpDoc)

        self.menuItemCheckUpdate = MenuItem(self.menuHelp, ID_ANY, u"检查更新(&U)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemCheckUpdate)

        self.menuItemAbout = MenuItem(self.menuHelp, ID_ANY, u"关于(&A)", EmptyString, ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemAbout)

        self.menuBar.Append(self.menuHelp, u"帮助(&H)")

        self.SetMenuBar(self.menuBar)

        self.statusBar = StatusBar(self, ID_ANY, STB_SIZEGRIP)
        statusBarFont = Font(10, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, False,
                             EmptyString)
        self.statusBar.SetFont(statusBarFont)
        self.SetStatusBar(self.statusBar)

        # self.statusBar = self.CreateStatusBar(1, STB_SIZEGRIP, ID_ANY)
        bSizer1 = BoxSizer(HORIZONTAL)

        self.hostsTree = TreeCtrl(
            self, ID_ANY,
            Point(0, 0),
            Size(size[0] / 9, -1),
            TR_DEFAULT_STYLE
        )
        bSizer1.Add(self.hostsTree, 0, EXPAND, 5)

        # self.hostsListView = CheckListBox(self, size=Size(size[0] / 9, -1))
        # bSizer1.Add(self.hostsListView, 0, EXPAND, 5)

        # WARNING: wxPython code generation isn't supported for this widget yet.
        self.codeEditor = CodeView(self)
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

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnMenuClicked(self, event):
        event.Skip()


###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog(Dialog):

    def __init__(self, parent):
        Dialog.__init__(
            self, parent,
            id=ID_ANY,
            title=u" 关于 mHosts - v%s" % version,
            pos=DefaultPosition,
            style=DEFAULT_DIALOG_STYLE
        )
        size = DisplaySize()
        self.SetSize(self.ConvertDialogToPixels(Size(400, 300)))
        self.SetSizeHints(DefaultSize, DefaultSize)
        self.SetIcon(Icon(iconPath, BITMAP_TYPE_ICO))
        bSizer2 = BoxSizer(VERTICAL)

        self.htmlWindow = HtmlView(self)
        bSizer2.Add(self.htmlWindow, 0, EXPAND, 0)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(BOTH)

    def __del__(self):
        pass
