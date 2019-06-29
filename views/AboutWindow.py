from wx import ID_ANY, Dialog, DEFAULT_DIALOG_STYLE, DefaultSize, BoxSizer, \
    VERTICAL, DefaultPosition, Size, EXPAND, BOTH

from views.HtmlView import HtmlView
from widgets import AboutDialog


class AboutWindow(AboutDialog):
    def __init__(self, parent):
        Dialog.__init__(self, parent, id=ID_ANY, title=u"关于", pos=DefaultPosition, size=Size(400, 300),
                        style=DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(DefaultSize, DefaultSize)

        bSizer2 = BoxSizer(VERTICAL)

        self.htmlWindow = HtmlView()
        bSizer2.Add(self.htmlWindow, 0, EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(BOTH)

    def __del__(self):
        pass
