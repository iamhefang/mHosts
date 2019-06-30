from wx.stc import StyledTextCtrl, STC_MARGIN_NUMBER, STC_STYLE_LINENUMBER, STC_STYLE_DEFAULT


class CodeView(StyledTextCtrl):
    def __init__(self, parent=None):
        StyledTextCtrl.__init__(self, parent)
        # 设置字体
        self.StyleSetSpec(STC_STYLE_DEFAULT, "face:Consolas,size:10")
        # 设置显示行号
        self.SetMarginType(0, STC_MARGIN_NUMBER)
        # 设置行号显示区域宽度
        self.SetMarginWidth(0, self.TextWidth(STC_STYLE_LINENUMBER, u"_99999"))
        # 不显示换行符
        self.SetViewEOL(False)
        # 不显示空白字符
        self.SetViewWhiteSpace(False)
