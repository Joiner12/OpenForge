# -*- coding: UTF-8 -*-
'''
@Author: chenjianwen
@Date: 2020-06-03 15:15:27
@LastEditTime: 2020-06-13 11:26:45
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \DsafeshareClient\mask_module.py
'''
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QMovie

import threading, queue
import time
import sys, signal


class M_mask(QWidget):

    def mouseMoveEvent(self, QMouseEvent):
        QMouseEvent.accept()

    sig_resize = pyqtSignal(int, int)

    def __init__(self, l="", h=""):
        super(M_mask, self).__init__()
        if l == "":
            l = 640
        if h == "":
            h = 512
        self.resize(l, h)
        self.m_ui()
        self.raise_()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  #置顶

    def m_ui(self):
        self.setWindowTitle("加载gif动画")
        self.label_01()

    def label_01(self):
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.m_movie()

    def m_movie(self):
        self.movie = QMovie("./imgs/0.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height())
