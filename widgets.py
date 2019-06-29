# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.html
import wx.xrc
###########################################################################
## Class MainFrame
###########################################################################
from wx import stc


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"mHosts - v0.0.1", pos=wx.DefaultPosition,
                          size=wx.Size(700, 500), style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(600, 400), wx.DefaultSize)

        self.menuBar = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.menuItemNew = wx.MenuItem(self.menuFile, wx.ID_ANY, u"新建(&N)", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuItemNew)

        self.menuFile.AppendSeparator()

        self.menuItemExit = wx.MenuItem(self.menuFile, wx.ID_ANY, u"退出(&Q)", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuItemExit)

        self.menuBar.Append(self.menuFile, u"文件(&F)")

        self.menuHelp = wx.Menu()
        self.menuItemCheckUpdate = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"检查更新(&U)", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemCheckUpdate)

        self.menuItemAbout = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"关于(&A)", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuHelp.Append(self.menuItemAbout)

        self.menuBar.Append(self.menuHelp, u"帮助(&H)")

        self.SetMenuBar(self.menuBar)

        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.hostsTree = wx.TreeCtrl(self, wx.ID_ANY, wx.Point(0, 0), wx.Size(200, -1), wx.TR_DEFAULT_STYLE)
        bSizer1.Add(self.hostsTree, 0, wx.EXPAND, 5)

        # WARNING: wxPython code generation isn't supported for this widget yet.
        self.codeEditor = stc.StyledTextCtrl(self)
        bSizer1.Add(self.codeEditor, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.OnMenuClicked, id=self.menuItemNew.GetId())
        self.Bind(wx.EVT_MENU, self.OnMenuClicked, id=self.menuItemExit.GetId())
        self.Bind(wx.EVT_MENU, self.OnMenuClicked, id=self.menuItemAbout.GetId())

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnMenuClicked(self, event):
        event.Skip()


###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"关于", pos=wx.DefaultPosition, size=wx.Size(400, 300),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.htmlWindow = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, 300),
                                             wx.html.HW_SCROLLBAR_AUTO)
        bSizer2.Add(self.htmlWindow, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
