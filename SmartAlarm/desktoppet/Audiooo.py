from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class PlayerThread(QThread):
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


app = QApplication([])

thread1 = PlayerThread(
    r'D:\Code\SmartAlarm\ikun_keyboard_catcher\audios\qmzzr.mp3')
# thread2 = PlayerThread('music2.mp3')

thread1.start()
# thread2.start()

# 主线程继续执行其他任务
while True:
    # do something
    pass
