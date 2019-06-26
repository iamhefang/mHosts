# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.richtext
import wx.xrc


###########################################################################
## Class MainWindow
###########################################################################

class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"mHosts", pos=wx.DefaultPosition, size=wx.Size(600, 400),
                          style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(600, 400), wx.DefaultSize)

        self.menuBar = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.menuItemNew = wx.MenuItem(self.menuFile, wx.ID_ANY, u"新建", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuItemNew)

        self.menuFile.AppendSeparator()

        self.menuItemExit = wx.MenuItem(self.menuFile, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuItemExit)

        self.menuBar.Append(self.menuFile, u"文件")

        self.menuHelp = wx.Menu()
        self.menuItemAbout = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"关于", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemAbout)

        self.menuBar.Append(self.menuHelp, u"帮助")

        self.SetMenuBar(self.menuBar)

        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.hostsTree = wx.TreeCtrl(self, wx.ID_ANY, wx.Point(0, 0), wx.Size(200, -1), wx.TR_DEFAULT_STYLE)
        bSizer1.Add(self.hostsTree, 0, wx.EXPAND, 5)

        self.codeEditor = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                   0 | wx.VSCROLL | wx.HSCROLL | wx.WANTS_CHARS | wx.BORDER_NONE)
        self.codeEditor.SetFont(
            wx.Font(11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Consolas"))

        bSizer1.Add(self.codeEditor, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.OnExitMenuSelection, id=self.menuItemExit.GetId())
        self.Bind(wx.EVT_MENU, self.OnAboutMenuSelection, id=self.menuItemAbout.GetId())

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnExitMenuSelection(self, event):
        event.Skip()

    def OnAboutMenuSelection(self, event):
        event.Skip()
