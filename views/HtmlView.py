from wx import ID_ANY, DefaultPosition, Size, html, LaunchDefaultBrowser
from wx.html import HtmlWindow

from helpers import FetchCurrentVersion


class HtmlView(HtmlWindow):
    def __init__(self):
        HtmlWindow.__init__(self, ID_ANY, DefaultPosition, Size(400, 300), html.HW_SCROLLBAR_AUTO)
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
            "version": FetchCurrentVersion()
        })

    def OnLinkClicked(self, link):
        LaunchDefaultBrowser(link.GetHref())
