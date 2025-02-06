#-*- coding:utf-8 -*-
"""
    主函数
"""
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QCursor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# import time

import functools


"""
    启动画面
    功能:
        1.启动过程播放启动动画和声音
        2.阻塞式实现
"""


class StartUp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        # set qmovie as label
        self.GifLabel = QLabel()
        self.movie = QMovie(r"./imgs/qmzzr-1.gif")
        self.GifLabel.setMovie(self.movie)
        # self.resize(400, 400)
        # self.setGeometry(1, 1, 100, 100)
        # self.setMinimumSize(QSize(200, 200))
        # self.setMaximumSize(QSize(200, 200))

    def Play(self):
        # 创建label组件

        print("play")
        self.movie.start()
        self.show()


"""
    自定义播放器
"""


class MyPlayer():

    def __init__(self, AudioFile=r"./audios/qmzzr.mp3") -> None:
        # 音频
        url = QUrl.fromLocalFile(AudioFile)
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.setVolume(100)

        # self.player.durationChanged.connect(self.get_time)
        # self.player.positionChanged.connect(self.get_time)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

        # 获取获得进度条进度
    def get_time(self):
        print('change')


class MainWindowKun(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.StartUpFunc()
        self.InitMainWindow()
        self.init_resources()
        # 键盘监听
        self.KBListener = KeyBoardListener(
            on_press_func=self.on_press,
            on_release_func=self.on_release,
            hot_keys_func_map=self.hot_keys_func_map)
        self.icon_quit()

    def init_resources(self):
        self.img_close_mouth = QPixmap(os.path.join("imgs", "cai1.png"))
        self.img_open_mouth = QPixmap(os.path.join("imgs", "cai2.png"))
        # 字母与音频对应关系
        self.ch2audio = {
            'j': os.path.join("audios", "j.mp3"),
            'n': os.path.join("audios", "n.mp3"),
            't': os.path.join("audios", "t.mp3"),
            'm': os.path.join("audios", "m.mp3"),
            'J': os.path.join("audios", "j.mp3"),
            'N': os.path.join("audios", "n.mp3"),
            'T': os.path.join("audios", "t.mp3"),
            'M': os.path.join("audios", "m.mp3"),
            'jntm': os.path.join("audios", "ngm.mp3")
        }
        self.hot_keys_func_map = {
            "<ctrl>+j":
            functools.partial(self.dosomething, path=self.ch2audio["jntm"])
            # "<ctrl>+j": self.play_ngm
        }

    """
        窗口初始化
    """

    def InitMainWindow(self):
        # 初始窗口设置大一点以免放入的图片显示不全
        self.pet_width = 400
        self.pet_height = 400
        # 获取桌面桌面大小决定宠物的初始位置为右上角
        desktop = QApplication.desktop()
        self.x = int(desktop.width() / 2 - self.pet_width / 2)
        self.y = int(desktop.height() / 2 - self.pet_height / 2)
        self.setGeometry(self.x, self.y, self.pet_width, self.pet_height)
        self.setWindowTitle('iKun')
        self.setWindowIcon(QIcon(r'./imgs/kun_keyboard.ico'))

        # 设置窗口为 无边框 | 保持顶部显示 | 任务栏不显示图标
        if True:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                                | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                                | Qt.WindowType.WindowStaysOnTopHint
                                | Qt.WindowType.SplashScreen)
        # 设置窗口透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.show()

    def dosomething(self):
        pass

    """
        启动软件界面
    """

    def StartUpFunc(self):
        # 定时器
        self.StartCounter = 0
        self.StartUpTimer = QTimer()
        self.StartUpTimer.timeout.connect(self.__StartUpTimeOutFunc)
        self.StartUpTimer.start(10)  # 10ms
        # 创建label组件
        self.labelMainPic = QLabel(self)
        self.labelMainPic.setAlignment(Qt.AlignCenter)
        self.labelMainPic.setGeometry(1, 1, 400, 400)

        # set qmovie as label
        self.movie = QMovie(r"./imgs/qmzzr-1.gif")
        self.labelMainPic.setMovie(self.movie)
        # 音频
        self.playerQmzzr = MyPlayer()
        self.playerQmzzr.play()
        self.movie.start()

    """
        启动软件信号控制
    """

    def __StartUpTimeOutFunc(self):
        self.StartCounter += 1
        if self.StartCounter > 50:
            # 停止播放
            self.movie.stop()

        if self.StartCounter > 100:
            self.StartUpTimer.stop()
            # GIF 不可见 切换图片
            if False:
                self.labelMainPic.setHidden(True)
            # 画面移动到右上角
            desktop = QApplication.desktop()
            self.x = desktop.width() - self.pet_width
            self.y = 1
            self.setGeometry(self.x, self.y, self.pet_width, self.pet_height)
            self.labelMainPic.setPixmap(QPixmap(r"./imgs/cai1.png"))
            self.KBListener.start_monitor()

    """
        窗口拖动功能
    """

    # 此函数和mouseMoveEvent配合可以完成拖动功能
    # 鼠标左键按下的时候获取当前位置
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            self.pos_first = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    # 设置可以拖动
    def mouseMoveEvent(self, QMouseEvent):
        self.move(QMouseEvent.globalPos() - self.pos_first)
        QMouseEvent.accept()

    """
        托盘功能
    """

    def icon_quit(self):
        # 托盘
        mini_icon = QSystemTrayIcon(self)
        mini_icon.setIcon(QIcon(r"./imgs/cai2.png"))
        mini_icon.setToolTip("小黑子 露出🐔脚了吧！")
        # 为托盘增加一个菜单选项
        tpMenu = QMenu(self)
        # 退出
        quit_menu = QAction('退出', self, triggered=self._quit)
        tpMenu.addAction(quit_menu)

        mini_icon.setContextMenu(tpMenu)
        mini_icon.show()

    """
        键盘监听回调函数
    """

    # 松开键盘时
    def on_release(self, key):
        # 闭嘴
        # self.lab.setPixmap(self.img_close_mouth)
        pass

    # 摁下键盘时
    def on_press(self, key):
        try:
            ch = key.char
        except AttributeError:
            ch = key.name
        # self.set_char(ch)
        print(ch)

    # def hot_keys_func_map(self, h):
    #     pass
    """
        退出函数
    """

    def _quit(self):
        self.close()
        self.KBListener.stop_monitor()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindowKun()
    sys.exit(app.exec_())