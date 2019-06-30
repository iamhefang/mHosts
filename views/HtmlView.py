from wx import ID_ANY, DefaultPosition, Size, html, LaunchDefaultBrowser
from wx.html import HtmlWindow

from version import version


class HtmlView(HtmlWindow):
    def __init__(self, parent):
        HtmlWindow.__init__(self, parent, ID_ANY, DefaultPosition, style=html.HW_SCROLLBAR_AUTO)
        self.SetSize(self.ConvertDialogToPixels(Size(400, 300)))
        self.SetPage("""
<!doctype html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>关于</title>
</head>
<body>
<h1>mHosts %(version)s</h1>
<h2>好用的跨平台Hosts管理工具</h2>
</body>
</html>""" % {
            "version": version
        })

    def OnLinkClicked(self, link):
        LaunchDefaultBrowser(link.GetHref())
