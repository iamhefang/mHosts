from distutils.version import LooseVersion
from threading import Thread, Lock, Event

from wx import MessageBox, ICON_ERROR, LaunchDefaultBrowser

from src.helpers import FetchNewVersion, Now
from src.settings import Settings


class CheckNewVersionThread(Thread):
    __window = None
    __threadLock = Lock()
    __event = Event()
    pool = []

    def __init__(self, window):
        Thread.__init__(self, name="CheckNewVersion")
        self.__window = window
        CheckNewVersionThread.pool.append(self)

    def run(self) -> None:
        try:
            self.__threadLock.acquire()
            self.__window.statusBar.SetStatusText("正在检查更新...", 2)
            self.__threadLock.release()
            newInfo = FetchNewVersion()
            newVersion = LooseVersion(newInfo['version'])
            currentVersion = LooseVersion(Settings.version())
            self.__threadLock.acquire()
            Settings.settings["lastCheckUpdateTime"] = Now()
            if currentVersion < newVersion:
                MessageBox("当前版本为%s, 检查到新版本%s" % (Settings.version(), newInfo["version"]))
                if newInfo["registry"]["type"] == "list":
                    LaunchDefaultBrowser(newInfo["registry"]["url"])
                self.__window.statusBar.SetStatusText("检查到新版本" + newInfo['version'], 2)
            else:
                self.__window.statusBar.SetStatusText("当前版本为最新版本", 2)
            self.__threadLock.release()
        except Exception as e:
            self.__window.statusBar.SetStatusText("", 2)
            self.__threadLock.acquire()
            self.__window.statusBar.SetStatusText("检查更新出错", 2)
            MessageBox(str(e), "检查更新时出现错误", ICON_ERROR)
            self.__threadLock.release()

    def stop(self):
        self.__event.set()
