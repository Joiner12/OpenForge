import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import QMainWindow, QSplashScreen, QLabel


class MySplashScreen(QSplashScreen):
    """
    设置开机动画
    """

    def __init__(self):
        super(MySplashScreen, self).__init__()

        # 新建动画
        self.movie = QMovie(
            r'D:\Code\SmartAlarm\desktoppet\resources\animation.gif')
        self.movie.frameChanged.connect(
            lambda: self.setPixmap(self.movie.currentPixmap()))
        self.movie.start()
        self.setFont(QFont('微软雅黑', 10))  # 设置字体
        self.show()

    def mousePressEvent(self, QMouseEvent):
        pass


class SplashDelay(QObject):
    """
        通过多线程实现开机动画延时
    """
    finished_signal = pyqtSignal()

    def __init__(self, delay_time_s=1):
        super(QObject, self).__init__()
        self.delay_time_s = delay_time_s

    def splash_delay_run(self):
        k = 0
        while k < self.delay_time_s * 100:
            time.sleep(0.01)
            k += 1
        self.finished_signal.emit()


class Form(QMainWindow):

    def __init__(self, splash):
        super(Form, self).__init__()
        self.resize(800, 600)

        self.splash = splash

        self.load_thread = QThread()
        self.load_worker = SplashDelay()
        self.load_worker.moveToThread(self.load_thread)
        self.load_thread.started.connect(self.load_worker.splash_delay_run)
        self.load_worker.finished_signal.connect(self.load_worker_finished)
        self.load_thread.start()

        while self.load_thread.isRunning():
            QtWidgets.qApp.processEvents()  # 不断刷新，保证动画流畅

        self.load_thread.deleteLater()
        # # 主窗口
        # self.gif_label = QLabel()
        # movie = QMovie(
        #     r'D:\Code\SmartAlarm\desktoppet\resources\animation.gif')
        # self.gif_label.setMovie(movie)
        # self.gif_label.show()
        # movie.start()
        self.show()

    def load_worker_finished(self):
        self.load_thread.quit()
        self.load_thread.wait()

    def set_message(self, message):
        self.splash.showMessage(message, Qt.AlignLeft | Qt.AlignBottom,
                                Qt.white)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    splash = MySplashScreen()

    app.processEvents()  # 处理主进程，不卡顿
    form = Form(splash)
    splash.finish(form)  # 主界面加载完成后隐藏
    splash.movie.stop()  # 停止动画
    splash.deleteLater()
    app.exec_()