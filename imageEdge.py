#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Edge(QWidget):

    def __init__(self):
        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        self.backImg = self.img
        self.w, self.h = 600, 400
        super().__init__()
        self.initUI()

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
        self.setWindowTitle("图像边缘检测系统")
        _palette = QPalette()
        _palette.setColor(QPalette.Background, QColor(192, 234, 123))
        self.setPalette(_palette)

    def createFunc(self):
        # 创建处理功能1
        self.name1 = QLabel()
        self.name1.setText("Sobel边缘检测:")
        # 设置单选按钮
        self.checkbox1 = QCheckBox("水平方向")
        self.checkbox1.setChecked(False)
        self.checkbox2 = QCheckBox("垂直方向")
        self.checkbox2.setChecked(False)
        # 创建处理功能2
        self.name2 = QLabel()
        self.name2.setText("laplacian边缘检测:")
        # 设置滑动条
        self.s1 = QSlider(Qt.Horizontal)
        self.s1.setMinimum(1)
        self.s1.setMaximum(11)
        self.s1.setSingleStep(1)
        # 创建处理功能3
        self.name3 = QLabel()
        self.name3.setText("Canny边缘检测:")
        # 设置输入框
        self.s2 = QSlider(Qt.Horizontal)
        self.s2.setMinimum(0)
        self.s2.setMaximum(255)
        self.s2.setSingleStep(1)
        self.s3 = QSlider(Qt.Horizontal)
        self.s3.setMinimum(0)
        self.s3.setMaximum(255)
        self.s3.setSingleStep(3)
        # 创建打开与保存
        self.btnOpen = QPushButton("打开", self)
        self.btnBack = QPushButton("还原", self)
        self.btnSave = QPushButton("保存", self)
        # 设置图片区域
        self.label = QLabel()

    def activateFunc(self):
        # 布局设定
        self.main_layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QHBoxLayout()
        # 第一部分布局
        self.layout1.addWidget(self.name1)
        self.layout1.addWidget(self.checkbox1)
        self.layout1.addWidget(self.checkbox2)
        # 第二部分布局
        self.layout2.addWidget(self.name2)
        self.layout2.addWidget(self.s1)
        # 第三部分布局
        self.layout3.addWidget(self.name3)
        self.layout3.addWidget(self.s2)
        self.layout3.addWidget(self.s3)
        # 第四部分布局
        self.layout4.addWidget(self.btnOpen)
        self.layout4.addWidget(self.btnBack)
        self.layout4.addWidget(self.btnSave)
        # 全局布局
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)
        self.main_layout.addLayout(self.layout3)
        self.main_layout.addLayout(self.layout4)
        self.setLayout(self.main_layout)
        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.checkbox1.stateChanged.connect(self.Sobel)
        self.checkbox2.stateChanged.connect(self.Sobel)
        self.s1.valueChanged.connect(self.Laplacian)
        self.s2.valueChanged.connect(self.Canny)
        self.s3.valueChanged.connect(self.Canny)
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnBack.clicked.connect(self.back)
        self.btnSave.clicked.connect(self.saveSlot)

    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, "Open Image", "./__data", "*.png *.jpg *.bmp")
        if fileName is "":
            return
        # 采用opencv函数读取数据
        self.img = cv2.imread(fileName, -1)
        if self.img.size == 1:
            return
        # 防止图片过大
        if self.img.shape[0] > self.w or self.img.shape[1] > self.h:
            if self.img.shape[1] < self.img.shape[0]:
                self.img = cv2.resize(self.img, (self.img.shape[1]//(self.img.shape[1]//self.h), self.img.shape[0]//(self.img.shape[0]//self.w)))
            else:
                self.img = cv2.resize(self.img, (self.img.shape[0]//(self.img.shape[0]//self.h), self.img.shape[1]//(self.img.shape[1]//self.w)))
        self.backImg = self.img
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.refreshShow()

    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, "Save Image", "./__data", "*.png *.jpg *.bmp", "*.png")
        if fileName is "":
            return
        if self.tempImg.size == 1:
            return
        # 调用opencv写入图像
        cv2.imwrite(fileName, self.tempImg)

    def back(self):
        # 还原图片
        self.img = self.backImg
        self.refreshShow()

    def Sobel(self):
        # Sobel边缘检测
        if self.img.size == 1:
            return
        # 框的状态
        if self.checkbox1.isChecked() and self.checkbox2.isChecked():
            # 水平垂直均检测
            xy = cv2.Sobel(self.gray, cv2.CV_64F, 1, 1, ksize=3)
            res = cv2.convertScaleAbs(xy)
        elif self.checkbox1.isChecked():
            # 执行水平方向检测
            x = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
            res = cv2.convertScaleAbs(x)
        elif self.checkbox2.isChecked():
            # 执行垂直方向检测
            y = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)
            res = cv2.convertScaleAbs(y)
        else:
            res = self.img
        self.tempImg = res
        self.refreshShow(aimImg=res, flag=True)

    def Laplacian(self):
        # Laplacian边缘检测
        if self.img.size == 1:
            return
        # 获取核大小
        n = int(self.s1.value())
        if n % 2 == 0:
            n += 1
        gray = cv2.GaussianBlur(self.gray, (5, 5), 0)
        res = cv2.Laplacian(gray, cv2.CV_16S, ksize=n)
        res = cv2.convertScaleAbs(res)
        self.tempImg = res
        self.refreshShow(aimImg=res, flag=True)

    def Canny(self):
        # Canny边缘检测
        if self.img.size == 1:
            return
        gray = cv2.GaussianBlur(self.gray, (3, 3), 0)
        # 提取阈值范围
        a = int(self.s2.value())
        b = int(self.s3.value())
        # 执行平滑操作
        if a > b:
            res = cv2.Canny(gray, b, a)
        else:
            res = cv2.Canny(gray, a, b)
        self.tempImg = res
        self.refreshShow(aimImg=res, flag=True)

    def refreshShow(self, aimImg=None, flag=False):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        if flag:
            img = aimImg
        else:
            img = self.img
        height, width = img.shape[0], img.shape[1]
        if len(img.shape) == 3:
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        else:
            bytesPerLine = width
            qImg = QImage(img.data, width, height, bytesPerLine,
                               QImage.Format_Grayscale8).rgbSwapped()
        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(qImg))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = Edge()
    w.show()
    sys.exit(a.exec_())






