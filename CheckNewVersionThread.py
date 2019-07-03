from distutils.version import LooseVersion
from threading import Thread, Lock, Event

from wx import MessageBox, ICON_ERROR

from helpers import FetchNewVersion
from settings import Settings


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
            if currentVersion < newVersion:
                self.__window.statusBar.SetStatusText("检查到新版本" + newVersion.vstring, 2)
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
