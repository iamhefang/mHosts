from threading import Thread, Event, Lock


class BackgroundThread(Thread):
    __callbackRun = None
    __callbackStop = None
    __event = Event()
    __pool = []
    threadLock = Lock()

    def __init__(self, run, stop=None):
        Thread.__init__(self)
        self.__callbackRun = run
        self.__callbackStop = stop
        BackgroundThread.__pool.append(self)

    def run(self) -> None:
        if callable(self.__callbackRun):
            self.__callbackRun()

    def stop(self):
        self.__event.set()
        if callable(self.__callbackStop):
            self.__callbackStop()

    @staticmethod
    def stopAllBackThread():
        for th in BackgroundThread.__pool:
            th.stop()
