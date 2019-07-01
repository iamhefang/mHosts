from wx import EVT_KEY_UP
from wx.stc import StyledTextCtrl, STC_MARGIN_NUMBER, STC_STYLE_LINENUMBER, STC_STYLE_DEFAULT


class CodeView(StyledTextCtrl):
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

        self.Bind(EVT_KEY_UP, self.OnKeyUp)

    def OnKeyUp(self, event):
        # 切换注释
        if event.controlDown and event.KeyCode == 47:
            print(event)
            print(self)
            pass
