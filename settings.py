import json
import os

from wx import Now

import Hosts
from helpers import WriteText, GetChromePath, ResPath

settingPath = "settings.json"


def hostsDict(
        hostId, name,
        readOnly=False, alwaysApply=False,
        url=None, lastUpdateTime=None,
        active=False, content=""):
    """
    封装Hosts字典
    :param hostId: hosts Id
    :param name: 名称
    :param readOnly: 是否只读
    :param alwaysApply: 是否公共hosts
    :param url: 在线hosts的url, 若不是在线hosts, 则该字段为None
    :param lastUpdateTime: 在线hosts的上次更新时间, 本地hosts的上次修改时间
    :param active: 是否为当前应用的hosts
    :param content: 内容
    :return: Dict
    """
    return {
        "id": hostId,
        "name": name,
        "readOnly": readOnly,
        "alwaysApply": alwaysApply,
        "url": url,
        "lastUpdateTime": lastUpdateTime,
        "active": active,
        "content": content
    }


ID_SYSTEM_HOSTS = 32767

systemHosts = hostsDict(ID_SYSTEM_HOSTS, "当前系统", readOnly=True, content="")


class Settings:
    __default = {
        "chromePath": GetChromePath(),
        "hostsPath": Hosts.GetHostsPath(),
        "hosts": [
            hostsDict(0x1994, u"公共", content=u"# 这是是公共hosts, 其他hosts应用时会自动把该hosts放到最前面\n", alwaysApply=True),
            hostsDict(0x1995, u"开发环境", content=u"# 开发环境\n"),
            hostsDict(0x1996, u"生产环境", content=u"# 生产环境\n")
        ],
        "rules": [
            {
                "title": u"方案1",
                "hosts": ["公共", "系统默认"]
            }
        ],
        "lastSaveTime": Now()
    }
    __version = None
    settings = None

    @staticmethod
    def version():
        if not Settings.__version:
            with open(ResPath("mHosts.json"), mode="r") as file:
                info = json.load(file)
                Settings.__version = info['version']
        return Settings.__version

    @staticmethod
    def Save():
        if not Settings.settings:
            Settings.Init()
        Settings.settings["lastSaveTime"] = Now()
        WriteText(settingPath, json.dumps(Settings.settings, ensure_ascii=False, indent=4))

    @staticmethod
    def Init():
        if not os.path.isfile(settingPath):
            WriteText(settingPath, json.dumps(Settings.__default, ensure_ascii=False, indent=4))
        with open(settingPath, mode="r", encoding="utf-8") as file:
            Settings.settings = json.load(file)
