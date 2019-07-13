from wx import ID_ANY, DefaultPosition, html, LaunchDefaultBrowser
from wx.html import HtmlWindow

from src.settings import Settings


class AboutView(HtmlWindow):
    def __init__(self, parent, size):
        HtmlWindow.__init__(self, parent, ID_ANY, DefaultPosition, size=size, style=html.HW_SCROLLBAR_AUTO)
        params = {
            "version": Settings.version()
        }
        self.SetPage(u"""
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
<h4>免费好用的跨平台Hosts管理工具</h4>
<table style="width:100%%">
<tr>
    <td style='text-align: right;'>作者:</td>
    <td><a href="https://hefang.link/?from=mHostsv%(version)s" title="点击访问何方博客">何方</a></td>
</tr>
<tr>
    <td style='text-align: right;'>项目地址:</td>
    <td>
        <a href="https://github.com/iamhefang/mHosts">https://github.com/iamhefang/mHosts</a>
    </td>
</tr>
<tr>
    <td style='text-align: right;'>问题和建议:</td>
    <td>
        <a href="https://github.com/iamhefang/mHosts/issues">Issues</a>
    </td>
</tr>
</table>
</body>
</html>""" % params)

    def OnLinkClicked(self, link):
        LaunchDefaultBrowser(link.GetHref())
