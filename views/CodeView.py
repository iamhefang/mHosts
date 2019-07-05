from wx import EVT_KEY_UP
from wx.stc import StyledTextCtrl, STC_MARGIN_NUMBER, STC_STYLE_LINENUMBER, STC_STYLE_DEFAULT, EVT_STC_CHANGE


class CodeView(StyledTextCtrl):
    __hosts: dict = None

    def __init__(self, parent=None):
        StyledTextCtrl.__init__(self, parent)
        # 设置字体
        self.StyleSetSpec(STC_STYLE_DEFAULT, "face:Consolas,size:10")
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
        # 可编辑
        self.SetReadOnly(False)
        self.Bind(EVT_STC_CHANGE, self.OnChange)
        self.Bind(EVT_KEY_UP, self.OnCodeEditorKeyUp)

    def OnChange(self, event):
        pass

    def SetHosts(self, hosts: dict):
        self.__hosts = hosts

    def OnCodeEditorKeyUp(self, event):
        if event.cmdDown and event.KeyCode == 83:
            pass
        if self.__hosts:
            self.__hosts["content"] = self.GetValue()
