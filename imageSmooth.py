#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QSlider, QWidget, QAction, QApplication, QMainWindow, QVBoxLayout, QFileDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt


class Smooth(QMainWindow):
    def __init__(self):
        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        self.backImg = self.img
        self.w, self.h = 600, 400
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建打开功能组件
        btnOpen = QAction("打开", self)
        btnOpen.setStatusTip("选择要处理的图片")
        # 创建保存功能组件
        btnSave = QAction("保存", self)
        btnSave.setShortcut("Ctrl+S")
        btnSave.setStatusTip("保存当前图片")
        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件")
        fileMenu.addAction(btnOpen)
        fileMenu.addAction(btnSave)
        # 初始化界面
        self.setGeometry(400, 200, self.w, self.h)
        self.setWindowTitle("图像平滑系统")
        self.main_frame = QWidget()
        # 创建处理功能1
        self.name1 = QLabel()
        self.name1.setText("高斯平滑")
        # 设置滑动条1
        self.func_s1 = QSlider(Qt.Horizontal)
        self.func_s1.setMinimum(1)
        self.func_s1.setMaximum(19)
        self.func_s1.setSingleStep(2)
        # 创建处理功能2
        self.name2 = QLabel()
        self.name2.setText("均值平滑")
        # 设置滑动条2
        self.func_s2 = QSlider(Qt.Horizontal)
        self.func_s2.setMinimum(1)
        self.func_s2.setMaximum(19)
        self.func_s2.setSingleStep(2)
        # 创建处理功能3
        self.name3 = QLabel()
        self.name3.setText("中值平滑")
        # 设置滑动条3
        self.func_s3 = QSlider(Qt.Horizontal)
        self.func_s3.setMinimum(1)
        self.func_s3.setMaximum(19)
        self.func_s3.setSingleStep(2)
        self.label = QLabel()
        # 布局设定
        self.main_layout = QVBoxLayout()
        self.main_frame.setLayout(self.main_layout)
        # 添加组件
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.name1)
        self.main_layout.addWidget(self.func_s1)
        self.main_layout.addWidget(self.name2)
        self.main_layout.addWidget(self.func_s2)
        self.main_layout.addWidget(self.name3)
        self.main_layout.addWidget(self.func_s3)
        self.setCentralWidget(self.main_frame)
        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        btnOpen.triggered.connect(self.openSlot)
        btnSave.triggered.connect(self.saveSlot)
        self.func_s1.valueChanged.connect(self.gaussianBlur)
        self.func_s2.valueChanged.connect(self.averageBlur)
        self.func_s3.valueChanged.connect(self.middleBlur)

    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, "Open Image", "./__data", "*.png *.jpg *.bmp")
        if fileName is "":
            return
        # 采用opencv函数读取数据
        self.img = cv.imread(fileName, -1)
        if self.img.size == 1:
            return
        # 防止图片过大
        if self.img.shape[0] > self.w or self.img.shape[1] > self.h:
            self.img = cv.resize(self.img, (self.img.shape[1]//(self.img.shape[1]//self.h), self.img.shape[0]//(self.img.shape[0]//self.w)))
        self.backImg = self.img
        self.refreshShow()

    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, "Save Image", "./__data", "*.png *.jpg *.bmp", "*.png")
        if fileName is "":
            return
        if self.backImg.size == 1:
            return
        # 调用opencv写入图像
        cv.imwrite(fileName, self.backImg)

    def gaussianBlur(self):
        # 高斯平滑
        if self.img.size == 1:
            return
        # 提取算子大小的值
        n = int(self.func_s1.value())
        if n % 2 == 0:
            n = n + 1
        # 执行平滑操作
        res = cv.GaussianBlur(self.img, (n, n), 0)
        self.backImg = res
        self.refreshShow(aimImg=res, flag=True)

    def averageBlur(self):
        # 均值平滑
        if self.img.size == 1:
            return
        # 提取算子大小的值
        n = int(self.func_s2.value())
        if n % 2 == 0:
            n = n + 1
        # 执行平滑操作
        res = cv.blur(self.img, (n, n))
        self.backImg = res
        self.refreshShow(aimImg=res, flag=True)

    def middleBlur(self):
        # 中值平滑
        if self.img.size == 1:
            return
        # 提取算子大小的值
        n = int(self.func_s3.value())
        if n % 2 == 0:
            n = n + 1
        # 执行平滑操作
        res = cv.medianBlur(self.img, n)
        self.backImg = res
        self.refreshShow(aimImg=res, flag=True)

    def refreshShow(self, aimImg=None, flag=False):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        if flag:
            img = aimImg
        else:
            img = self.img
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(qImg))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = Smooth()
    w.show()
    sys.exit(a.exec_())