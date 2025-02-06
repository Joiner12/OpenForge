'''
    Function:
        桌面宠物
'''
import os
import sys
import time
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu, \
    QAction, QDesktopWidget, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, QObject, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QImage, QMovie, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
"""
配置信息
"""


class MySplashScreen(QSplashScreen):
    """
    设置开机动画
    """

    def __init__(self):
        super(MySplashScreen, self).__init__()
        # 软件启动动画
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
    delay_time_s = 10

    def __init__(self, delay_time=1):
        super(QObject, self).__init__()
        self.delay_time_s = delay_time
        # # 软件启动音频
        # player = QMediaPlayer()
        # url = QUrl.fromLocalFile(
        #     r"D:\Code\SmartAlarm\ikun_keyboard_catcher\audios\qmzzr.mp3")
        # player.setMedia(QMediaContent(url))
        # player.play()

    def splash_delay_run(self):
        k = 0
        while k < self.delay_time_s * 100:
            time.sleep(0.01)
            k += 1
        self.finished_signal.emit()


class PlayerThread(QThread):
    """
        多线程音频播放
    """
    finished = pyqtSignal()  # 自定义信号，用于通知主线程播放完成

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        player = QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(self.url)))
        player.play()
        while player.state() == QMediaPlayer.PlayingState:  # 等待音频播放完成
            self.sleep(1)
        player.stop()
        self.finished.emit()  # 发送finished信号


class Config():
    ROOT_DIR = os.path.join(
        os.path.split(os.path.abspath(__file__))[0], 'resources')
    ACTION_DISTRIBUTION = [['1', '2', '3'],
                           ['4', '5', '6', '7', '8', '9', '10', '11'],
                           ['12', '13', '14'], ['15', '16', '17'],
                           ['18', '19'], ['20', '21'], ['22'],
                           ['23', '24', '25'], ['26', '27', '28', '29'],
                           ['30', '31', '32', '33'], ['34', '35', '36', '37'],
                           ['38', '39', '40', '41'],
                           ['42', '43', '44', '45', '46']]
    PET_ACTIONS_MAP = dict()
    for name in ['pikachu', 'blackcat', 'whitecat', 'fox']:
        PET_ACTIONS_MAP[name] = ACTION_DISTRIBUTION
    PET_ACTIONS_MAP['bingdwendwen'] = [
        [str(i) for i in range(1, 41, 8)],
        [str(i) for i in range(41, 56)],
        [str(i) for i in range(56, 91)],
    ]


"""
    桌面宠物
"""


class DesktopPet(QWidget):
    tool_name = '桌面宠物'

    def __init__(self, pet_type='blackcat', parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.pet_type = pet_type
        self.cfg = Config()
        # 窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
                            | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 导入宠物
        if pet_type not in self.cfg.PET_ACTIONS_MAP:
            pet_type = None
        if pet_type is None:
            self.pet_images, iconpath = self.randomLoadPetImages()
        else:
            for name in list(self.cfg.PET_ACTIONS_MAP.keys()):
                if name != pet_type:
                    self.cfg.PET_ACTIONS_MAP.pop(name)
            self.pet_images, iconpath = self.randomLoadPetImages()
        # 设置退出选项
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(iconpath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        # 线程处理 启动动画 播放语音
        self.load_thread = QThread()  # 创建新线程
        self.play_thread = QThread()
        self.load_worker = SplashDelay(delay_time=5)
        self.playaudio = PlayerThread(
            r'D:\Code\SmartAlarm\ikun_keyboard_catcher\audios\qmzzr.mp3')
        self.load_worker.moveToThread(self.load_thread)  # 添加线程任务
        self.play_thread.moveToThread(self.playaudio)
        self.load_thread.started.connect(
            self.load_worker.splash_delay_run)  # 启动线程定时主循环
        self.play_thread.started.connect(self.playaudio.run)
        self.load_worker.finished_signal.connect(
            self.load_worker_finished)  # 线程定时结束信号
        self.load_thread.start()  # 启动线程

        while self.load_thread.isRunning():
            QtWidgets.qApp.processEvents()  # 不断刷新，保证动画流畅

        self.load_thread.deleteLater()  # 删除线程
        self.playaudio.deleteLater()
        # 当前显示的图片
        self.image = QLabel(self)
        self.setImage(self.pet_images[0][0])
        # 是否跟随鼠标
        self.is_follow_mouse = False
        # 宠物拖拽时避免鼠标直接跳到左上角
        self.mouse_drag_pos = self.pos()
        # 显示
        self.resize(self.pet_images[0][0].size().width(),
                    self.pet_images[0][0].size().height())
        self.randomPosition()
        self.show()
        # 宠物动画动作执行所需的一些变量
        self.is_running_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0
        # 每隔一段时间做个动作
        self.timer_act = QTimer()
        self.timer_act.timeout.connect(self.randomAct)
        self.timer_act.start(200)

    '''启动动画完成'''

    def load_worker_finished(self):
        self.load_thread.quit()
        self.load_thread.wait()

    '''随机做一个动作'''

    def randomAct(self):
        if not self.is_running_action:
            self.is_running_action = True
            self.action_images = random.choice(self.pet_images)
            self.action_max_len = len(self.action_images)
            self.action_pointer = 0
        self.runFrame()

    '''完成动作的每一帧'''

    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1

    '''设置当前显示的图片'''

    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))

    '''随机导入一个桌面宠物的所有图片'''

    def randomLoadPetImages(self):
        cfg = self.cfg
        pet_name = random.choice(list(cfg.PET_ACTIONS_MAP.keys()))
        actions = cfg.PET_ACTIONS_MAP[pet_name]
        pet_images = []
        for action in actions:
            pet_images.append([
                self.loadImage(
                    os.path.join(cfg.ROOT_DIR, pet_name,
                                 'shime' + item + '.png')) for item in action
            ])
        iconpath = os.path.join(cfg.ROOT_DIR, pet_name, 'shime1.png')
        return pet_images, iconpath

    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    '''鼠标移动, 则宠物也移动'''

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''鼠标释放时, 取消绑定'''

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    '''导入图像'''

    def loadImage(self, imagepath):
        image = QImage()
        image.load(imagepath)
        return image

    '''随机到一个屏幕上的某个位置'''

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    '''退出程序'''

    def quit(self):
        self.close()
        sys.exit()


def main():
    app = QApplication(sys.argv)
    splash = MySplashScreen()

    app.processEvents()  # 处理主进程，不卡顿
    form = DesktopPet()
    form.show()
    splash.finish(form)  # 主界面加载完成后隐藏
    splash.movie.stop()  # 停止动画
    splash.deleteLater()
    app.exec_()


if __name__ == "__main__":
    main()
