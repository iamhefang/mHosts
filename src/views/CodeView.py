import os
import sys

from wx import EVT_KEY_DOWN, EVT_KEY_UP
from wx.stc import (
    EVT_STC_CHANGE, STC_LEX_CONF, STC_MARGIN_NUMBER,
    STC_P_CHARACTER, STC_P_CLASSNAME, STC_P_COMMENTLINE,
    STC_P_DEFAULT, STC_STYLE_DEFAULT, STC_STYLE_LINENUMBER,
    StyledTextCtrl
)

if sys.platform == 'win32':
    style = {
        'font': 'Consolas',
        'size': 10,
    }
elif sys.platform == 'darwin':
    style = {
        'font': 'Monaco',
        'size': 12,
    }
else:
    style = {
        'font': 'Consolas',
        'size': 12,
    }


class CodeView(StyledTextCtrl):
    __hosts: dict = None

    def __init__(self, parent=None, dpi=(1, 1)):
        StyledTextCtrl.__init__(self, parent)
        # 设置样式
        self.InitStyle()
        # 设置显示行号
        self.SetMarginType(0, STC_MARGIN_NUMBER)
        # 设置行号显示区域宽度
        self.SetMarginWidth(0, self.TextWidth(STC_STYLE_LINENUMBER, u"_9999"))
        # 不显示换行符
        self.SetViewEOL(False)
        # 不显示空白字符
        self.SetViewWhiteSpace(False)
        # 行号和内容之间留一定的间距
        self.SetMarginWidth(1, self.TextWidth(STC_STYLE_LINENUMBER, u"_"))
        self.SetEdgeColumn(80)
        self.SetScrollWidth(600 * dpi[0])
        # 可编辑
        self.SetReadOnly(False)

        self.Bind(EVT_STC_CHANGE, self.OnChange)
        self.Bind(EVT_KEY_UP, self.OnCodeEditorKeyUp)
        self.Bind(EVT_KEY_DOWN, self.OnKeyDown)

    def InitStyle(self):
        self.SetLexer(STC_LEX_CONF)
        # 默认字体
        self.StyleSetSpec(STC_STYLE_DEFAULT, "face:%(font)s,size:%(size)d,fore:#99ff99" % style)
        # 域名
        self.StyleSetSpec(
            STC_P_DEFAULT, "fore:#7F007F,face:%(font)s,size:%(size)d" % style)
        self.StyleSetSpec(
            STC_P_CHARACTER, "fore:#7F007F,face:%(font)s,size:%(size)d" % style)
        # 注释
        self.StyleSetSpec(STC_P_COMMENTLINE,
                          "fore:#999999,face:%(font)s,size:%(size)d" % style)
        # ip地址
        self.StyleSetSpec(
            STC_P_CLASSNAME, "fore:#0000FF,size:%(size)d" % style)

    def OnChange(self, event):
        pass

    def SetValue(self, value: str):
        StyledTextCtrl.SetValue(self, value.replace(os.linesep, "\n"))
        self.EmptyUndoBuffer()

    def SetHosts(self, hosts: dict):
        self.__hosts = hosts

    def OnKeyDown(self, event):
        if event.cmdDown and event.KeyCode == 47:
            # lineNumber = self.GetCurrentLine()
            # (CharBuffer, linePos) = self.GetCurLine()
            # self.InsertText(0, "#")
            pass
        else:
            event.Skip()

    def OnCodeEditorKeyUp(self, event):
        if self.__hosts:
            self.__hosts["content"] = self.GetValue()
