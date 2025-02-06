"""
装载Gif动画

QMovie
"""
import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


#自定义Splash类
class MySplash(QWidget):

    def __init__(self):
        super(MySplash, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)  #设置背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  #设置无边框
        self.setGeometry(700, 190, 800, 800)
        self.text = "初始化程序...0%"

    def paintEvent(self, QPaintEvent):
        self.p = QPainter(self)
        self.p.setPen(QPen())
        self.p.setBrush(QBrush())
        self.p.drawPixmap(
            0, 0,
            QPixmap("D:\Code\SmartAlarm\ikun_keyboard_catcher\imgs\cai2.png"
                    ))  #加载自己的图片
        self.p.drawText(QRect(26, 342, 200, 100), Qt.AlignCenter,
                        self.text)  #showMesage

    def setText(self, text):
        self.text = text
        self.paintEvent(QPaintEvent)


#启动界面显示时间的设置
def load_Message(splash):
    for i in range(1, 10):  # 显示时间4秒
        time.sleep(1)  # 睡眠
        splash.setText("初始化程序...{0}%".format(25 * i))
        splash.update()
        qApp.processEvents()


class LoadingGif(QWidget):

    def __init__(self):
        super(LoadingGif, self).__init__()
        self.label = QLabel("", self)
        self.setFixedSize(512, 512)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.movie = QMovie(
            "D:\Code\SmartAlarm\ikun_keyboard_catcher\imgs\sb.gif")
        self.label.setMovie(self.movie)
        self.movie.start()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    splash = MySplash()
    splash.show()  # 显示启动界面
    qApp.processEvents()
    LoadingGif()
    load_Message(splash)  # 加载文字进度信息
    splash.close()  # 隐藏启动界面
    sys.exit(app.exec_())
