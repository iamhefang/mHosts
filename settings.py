import json
import os

from Hosts import Hosts
from helpers import WriteText, GetChromePath

settingPath = "settings.json"


class Settings:
    __default = {
        "chrome-path": GetChromePath(),
        "hosts-path": Hosts.GetHostsPath(),
        "hosts": [
            {
                "name": u"系统默认",
                "readOnly": True,
                "alwaysApply": False,
                "url": None,
                "lastUpdateTime": None,
                "content": Hosts.GetSystemHosts()
            },
            {
                "name": u"公共",
                "readOnly": False,
                "alwaysApply": True,
                "url": None,
                "lastUpdateTime": None,
                "content": u"# 这是是公共hosts, 其他hosts应用时会自动把该hosts放到最前面\n"
            }
        ],
        "rules": [
            {
                "title": u"方案1",
                "hosts": ["公共", "系统默认"]
            }
        ]
    }
    settings = {}

    @staticmethod
    def Init():
        if not os.path.isfile(settingPath):
            WriteText(settingPath, json.dumps(Settings.__default, ensure_ascii=False, indent=4))
        with open(settingPath, mode="r", encoding="utf-8") as file:
            Settings.settings = json.load(file)
        print(Settings.settings)
