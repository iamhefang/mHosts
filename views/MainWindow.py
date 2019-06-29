import sys
import traceback

from wx import App, Icon, BITMAP_TYPE_ICO, MessageBox, ICON_ERROR, OK, ICON_NONE, stc, \
    SystemSettings, SYS_COLOUR_HIGHLIGHTTEXT, SYS_COLOUR_HIGHLIGHT, Colour
from wx.stc import STC_MARGIN_SYMBOL, STC_MASK_FOLDERS, STC_FOLDFLAG_LINEBEFORE_CONTRACTED, \
    STC_FOLDFLAG_LINEAFTER_CONTRACTED, STC_MARGIN_NUMBER, STC_STYLE_LINENUMBER, STC_MARKNUM_FOLDER, \
    STC_MARKNUM_FOLDEROPEN, STC_MARKNUM_FOLDERSUB, STC_MARK_BOXPLUS, \
    STC_MARKNUM_FOLDEREND, STC_MARK_BOXMINUS, \
    STC_MARKNUM_FOLDEROPENMID, STC_MARKNUM_FOLDERMIDTAIL, STC_MARKNUM_FOLDERTAIL, STC_MARK_EMPTY

from Hosts import Hosts
from helpers import FetchCurrentVersion
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

    def InitMainWindow(self):
        self.SetTitle(u"mHosts - v" + FetchCurrentVersion())
        self.SetIcon(Icon("icons/logo.ico", BITMAP_TYPE_ICO))
        self.Show()
        self.codeEditor.SetText(Hosts.GetSystemHosts())

    def InitHostView(self):
        self.codeEditor.StyleSetSpec(stc.STC_C_COMMENT, "fore: #00ff00")
        self.codeEditor.SetUseTabs(False)
        self.codeEditor.SetTabWidth(4)
        self.codeEditor.SetIndent(4)
        self.codeEditor.SetTabIndents(True)
        self.codeEditor.SetBackSpaceUnIndents(True)
        self.codeEditor.SetViewEOL(False)
        self.codeEditor.SetViewWhiteSpace(False)
        self.codeEditor.SetMarginWidth(2, 0)
        self.codeEditor.SetIndentationGuides(True)
        self.codeEditor.SetMarginType(1, STC_MARGIN_SYMBOL)
        self.codeEditor.SetMarginMask(1, STC_MASK_FOLDERS)
        self.codeEditor.SetMarginWidth(1, 16)
        self.codeEditor.SetMarginSensitive(1, True)
        self.codeEditor.SetProperty(u"fold", u"1")
        self.codeEditor.SetFoldFlags(STC_FOLDFLAG_LINEBEFORE_CONTRACTED | STC_FOLDFLAG_LINEAFTER_CONTRACTED)
        self.codeEditor.SetMarginType(0, STC_MARGIN_NUMBER)
        self.codeEditor.SetMarginWidth(0, self.codeEditor.TextWidth(STC_STYLE_LINENUMBER, u"_99999"))
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDER, STC_MARK_BOXPLUS)
        self.codeEditor.MarkerSetBackground(STC_MARKNUM_FOLDER, Colour(u"BLACK"))
        self.codeEditor.MarkerSetForeground(STC_MARKNUM_FOLDER, Colour(u"WHITE"))
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDEROPEN, STC_MARK_BOXMINUS)
        self.codeEditor.MarkerSetBackground(STC_MARKNUM_FOLDEROPEN, Colour(u"BLACK"))
        self.codeEditor.MarkerSetForeground(STC_MARKNUM_FOLDEROPEN, Colour(u"WHITE"))
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDERSUB, STC_MARK_EMPTY)
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDEREND, STC_MARK_BOXPLUS)
        self.codeEditor.MarkerSetBackground(STC_MARKNUM_FOLDEREND, Colour(u"BLACK"))
        self.codeEditor.MarkerSetForeground(STC_MARKNUM_FOLDEREND, Colour(u"WHITE"))
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDEROPENMID, STC_MARK_BOXMINUS)
        self.codeEditor.MarkerSetBackground(STC_MARKNUM_FOLDEROPENMID, Colour(u"BLACK"))
        self.codeEditor.MarkerSetForeground(STC_MARKNUM_FOLDEROPENMID, Colour(u"WHITE"))
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDERMIDTAIL, STC_MARK_EMPTY)
        self.codeEditor.MarkerDefine(STC_MARKNUM_FOLDERTAIL, STC_MARK_EMPTY)
        self.codeEditor.SetSelBackground(True, SystemSettings.GetColour(SYS_COLOUR_HIGHLIGHT))
        self.codeEditor.SetSelForeground(True, SystemSettings.GetColour(SYS_COLOUR_HIGHLIGHTTEXT))

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
        callback = {
                       self.menuItemExit.GetId(): self.Exit,
                       self.menuItemAbout.GetId(): self.ShowAboutDialog,
                       TrayIcon.ID_EXIT: self.Exit,
                       TrayIcon.ID_TOGGLE: self.ToggleWindow,
                       TrayIcon.ID_REFRESH_DNS: MainWindow.DoRefreshDNS,
                       TrayIcon.ID_NEW: None,
                       TrayIcon.ID_IMPORT: None
                   }[event.GetId()] or None

        if callback:
            callback()

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
        print("版本：", FetchCurrentVersion())
        print("系统：", sys.platform)
        print("hosts:", Hosts.GetHostsPath())
