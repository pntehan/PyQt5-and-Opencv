#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2020-05-21 14:58:39
# Author  : Pntehan


import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal
import time


class Edge(QWidget):

    def __init__(self):
        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        self.backImg = self.img
        self.w, self.h = 600, 400
        super().__init__()
        self.initUI()
        self.fastNum = 1

    def initUI(self):
        # 初始化窗口布局
        self.initLayout()
        # 创建功能组件
        self.createFunc()
        # 添加功能组件并激活
        self.activateFunc()

    def initLayout(self):
        # 初始化界面
        self.setGeometry(400, 200, self.w, self.h)
        self.setWindowTitle("视频播放系统")
        _palette = QPalette()
        _palette.setColor(QPalette.Background, QColor(192, 234, 123))
        self.setPalette(_palette)

    def createFunc(self):
        # 创建组件
        self.btnOpen = QPushButton("打开", self)
        self.btnCamera = QPushButton("调用摄像头", self)
        self.btnActivate = QPushButton("暂停", self)
        self.btnFaster = QPushButton("加速", self)
        self.progressbar = QProgressBar(self)
        # 设置图片区域
        self.video = QLabel()
        self.timer = QTimer()

    def activateFunc(self):
        # 布局设定
        self.main_layout = QVBoxLayout()
        self.layout = QHBoxLayout()
        # 布局
        self.layout.addWidget(self.btnOpen)
        self.layout.addWidget(self.btnCamera)
        self.layout.addWidget(self.btnActivate)
        self.layout.addWidget(self.btnFaster)
        # 全局布局
        self.main_layout.addWidget(self.video)
        self.main_layout.addWidget(self.progressbar)
        self.main_layout.addLayout(self.layout)
        self.setLayout(self.main_layout)
        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnCamera.clicked.connect(self.openCamera)
        self.btnActivate.clicked.connect(self.pauseSlot)
        self.btnFaster.clicked.connect(self.FasterSlot)

    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, "Open Video", "./__data", "*.mp4 *.avi *.flv")
        if fileName is "":
            return
        # 采用opencv函数读取数据
        self.cap = cv2.VideoCapture(fileName)
        self.fps = 1000 / int(self.cap.get(cv2.CAP_PROP_FPS))
        self.range = self.fps
        self.step = 0
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) * self.fps
        # 设置时间轴
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(self.length)
        self.timer.timeout.connect(self.play_video)
        self.timer.start(self.fps)

    def openCamera(self):
        # 采用opencv函数读取数据
        self.cap = cv2.VideoCapture(0)
        self.fps = 1000 / int(self.cap.get(cv2.CAP_PROP_FPS))
        self.range = self.fps
        self.step = 0
         # 设置时间轴
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(self.range)
        self.timer.timeout.connect(self.play_Camera)
        self.timer.start(self.fps)

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.step += self.range
            a = time.strftime("%M:%S", time.localtime(self.step/1000))
            b = time.strftime("%M:%S", time.localtime(self.length/1000))
            self.progressbar.setFormat("{}/{}".format(a, b))
            self.progressbar.setAlignment(Qt.AlignRight)
            self.progressbar.setValue(self.step)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine,
                               QImage.Format_RGB888).rgbSwapped()
            self.video.setAlignment(Qt.AlignCenter)
            self.video.setPixmap(QPixmap.fromImage(qImg))

    def play_Camera(self):
        ret, frame = self.cap.read()
        if ret:
            self.step += self.range
            a = time.strftime("%M:%S", time.localtime(self.step/1000))
            b = time.strftime("%M:%S", time.localtime(self.step/1000))
            self.progressbar.setFormat("{}/{}".format(a, b))
            self.progressbar.setAlignment(Qt.AlignRight)
            self.progressbar.setValue(self.step)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine,
                               QImage.Format_RGB888).rgbSwapped()
            self.video.setAlignment(Qt.AlignCenter)
            self.video.setPixmap(QPixmap.fromImage(qImg))

    def pauseSlot(self):
        self.btnActivate.setText("播放")
        self.btnActivate.clicked.connect(self.backSlot)
        self.timer.stop()

    def backSlot(self):
        self.btnActivate.setText("暂停")
        self.btnActivate.clicked.connect(self.pauseSlot)
        self.timer.start(self.fps)

    def FasterSlot(self):
        if self.fastNum == 32:
            self.fps = self.fps * 32
            self.btnFaster.setText("加速")
            self.fastNum = 1
            self.timer.start(self.fps)
        else:
            self.fps = self.fps // 2
            self.fastNum *= 2
            self.btnFaster.setText("{}倍速".format(self.fastNum))
            self.timer.start(self.fps)



if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = Edge()
    w.show()
    sys.exit(a.exec_())






