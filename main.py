# _*_ coding: utf-8 _*_
from views.MainWindow import MainWindow

if __name__ == '__main__':
    # try:
    MainWindow.PrintSysInfo()
    MainWindow().MainLoop()
# except BaseException as err:
#     print(err)
