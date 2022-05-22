#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import sys
import cv2
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Ui_MainWindow(QtWidgets.QWidget):

    def exist_dir(self, path):
        path = os.path.abspath(path)

        # 存在这个文件夹或路径
        if not os.path.exists(path):
            # 创建
            os.mkdir(path)

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        # self.img = object
        self.exist_dir('./Photos')
        self.tmpname = 'tmp'
        self.showImage = None
        self.hadsave = False
        self.allowsave = False
        self.right_exist = False
        self.allowdiscern = True

        self.issaving = False
        # 测试设置为True
        self.needtrain = True

        self.config_path = os.getcwd() + '\\config.ini'
        self.photodir_path = os.getcwd() + '\\Photos\\'

        from TakePhotos import TakeP
        self.tmp = TakeP()
        self.tmp.config_is_right()
        self.num = self.tmp.getConf_num() + 1
        self.tmpfilename = ''

        self.selectnum = [str(i) for i in range(1, self.num + 1)]

        self.filenum = [os.path.split(os.path.join(self.photodir_path, f))[1].split('.')[0] for f in
                        os.listdir(self.photodir_path)]

        self.selectnum = list(set(self.selectnum) - set(self.filenum))

        self.tmp.config_is_right()

    # UI模块
    def set_ui(self):
        font = QtGui.QFont()
        font.setFamily("kaiti")
        font.setPointSize(18)
        self.textBrowser = QtWidgets.QLabel("人脸检测系统")
        self.textBrowser.setAlignment(Qt.AlignCenter)
        self.textBrowser.setFont(font)
        self.mm_layout = QVBoxLayout()
        self.l_down_widget = QtWidgets.QWidget()
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_cap = QtWidgets.QPushButton(u'拍照')
        self.file = QtWidgets.QPushButton(u'打开文件')
        self.train = QtWidgets.QPushButton(u'图片训练')
        self.savepic = QtWidgets.QPushButton(u'保存图片或继续')
        self.discern = QtWidgets.QPushButton(u'开始检测')
        fontx = QtGui.QFont()
        fontx.setFamily("kaiti")
        fontx.setPointSize(16)

        # Button 的颜色修改
        button_color = [self.button_open_camera, self.button_cap, self.file, self.train, self.discern, self.savepic]

        for i in range(len(button_color)):
            button_color[i].setFont(fontx)
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_cap.setMinimumHeight(50)
        self.file.setMinimumHeight(50)
        self.discern.setMinimumHeight(50)
        self.train.setMinimumHeight(50)
        self.savepic.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)
        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        # 添加右侧组件
        self.__layout_fun_button.addWidget(self.file)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_cap)
        self.__layout_fun_button.addWidget(self.savepic)
        self.__layout_fun_button.addWidget(self.train)
        self.__layout_fun_button.addWidget(self.discern)
        self.__layout_fun_button.addWidget(self.label_move)

        # 添加一个右侧的组件
        self.right_widget = QWidget()
        self.right_widget_layout = QHBoxLayout()
        self.cap_label = QLabel()
        self.cap_label.setFixedSize(641, 481)
        self.cap_label.setAutoFillBackground(False)
        self.right_widget_layout.addWidget(self.label_show_camera)
        self.right_widget_layout.addWidget(self.cap_label)
        self.right_widget.setLayout(self.right_widget_layout)
        self.__layout_main.addWidget(self.right_widget)
        self.__layout_main.addLayout(self.__layout_fun_button)

        # 按钮居中显示
        # self.__layout_main.addWidget(self.label_show_camera)

        self.l_down_widget.setLayout(self.__layout_main)
        self.mm_layout.addWidget(self.textBrowser)
        self.mm_layout.addWidget(self.l_down_widget)
        self.setLayout(self.mm_layout)
        self.label_move.raise_()
        self.setWindowTitle(u'人脸检测系统')
        # self.setStyleSheet("#MainWindow{border-image:url(DD.png)}")

        '''
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

    # 槽函数链接初始化
    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_cap.clicked.connect(self.capx)
        self.file.clicked.connect(self.openSlot)
        self.savepic.clicked.connect(self.save)
        self.train.clicked.connect(self.Btrain)
        self.discern.clicked.connect(self.discernPic)

    # 识别
    def discernPic(self):
        trainpath = './Trainer/trainer.yml'
        if not os.path.exists(trainpath):
            print('文件不存在先训练')
            QMessageBox.warning(self, '警告', '请先训练')
            return

        if not self.allowdiscern or self.needtrain:
            QMessageBox.warning(self, '警告', '图片需要训练')
            return

        self.timer_camera.stop()
        self.cap.release()
        self.label_show_camera.clear()
        self.button_open_camera.setText(u'打开相机')

        from ShiBie import ShiBieObject

        tmp = ShiBieObject()
        tmp.run()

    # 训练
    def Btrain(self):

        if not os.listdir('./Photos'):
            QMessageBox.warning(self, '警告', '文件夹为空')
            return

        if not self.needtrain:
            QMessageBox.warning(self, '警告', '已经训练，不需要再进行训练。或者你需要先保存图片')
            return

        from TrainPhotos import Tra

        # 开始训练
        tt = Tra()
        tt.run()

        self.needtrain = False

        # 允许识别
        self.allowdiscern = True

        QMessageBox.information(self, '提示', '训练完成')

    def cvimg_to_qtimg(self, cvimg):
        h, w, d = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, w, h, w * d, QImage.Format_RGB888)
        return cvimg

    def openSlot(self):
        # 调用打开文件diglog
        fileName, filterr = QFileDialog.getOpenFileName(
            self, '导入照片', './Photos', '*.png *.jpg *.bmp')

        if fileName == '':
            return

        print('fileName', fileName)
        fileName2 = os.path.splitext(fileName)[0].replace('/', '\\') + os.path.splitext(fileName)[1]
        print('fileName2', fileName2)
        # print(os.path.splitext(fileName)[1])
        fileName = os.path.split(fileName)[1]
        # fileName = os.path.splitext(fileName)[1]

        print('fileName', fileName)
        # fileName.split('.')[-1]

        self.tmpname = fileName.split('.')[-2]
        print('tmp', self.tmpname)

        print('fileName2', fileName2)
        ###
        self.cap_label.setPixmap(QtGui.QPixmap(fileName2))
        self.right_exist = True
        self.allowsave = True
        self.hadsave = False

        self.tmpfilename = fileName2

        ##########
        cvimg = cv2.imread(fileName)

        self.showImage = cvimg

        if not self.timer_camera.isActive():
            self.tmpname = fileName

    # 打开摄像头
    def button_open_camera_click(self):

        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM, cv2.CAP_DSHOW)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:
                self.timer_camera.start(30)

                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')

    # 显示摄像头
    def show_camera(self):

        flag, self.image = self.cap.read()

        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

        if not self.issaving:
            self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))

    # 保存图片
    def save(self):
        self.issaving = True

        # 当前保存的序号
        # self.num += 1

        print('filenuj', self.filenum)
        print('seltc', self.selectnum)

        print('nu', self.num)

        for ii in range(self.num - 1):

            print('jinr')
            if self.filenum[ii] != self.selectnum[ii]:
                self.num = int(self.selectnum[ii])
                print('selectnum', self.num)
                break

        print('num', self.num)
        self.tmp.config_is_right()

        # path = self.photodir_path
        # imgpath = path + str(self.num) + '.' + self.tmpname + ".jpg"

        if self.hadsave:
            QMessageBox.warning(self, '警告', '图片已经保存')
            self.issaving = False
            return

        elif self.right_exist == False:
            QMessageBox.warning(self, '警告', '没有图片显示')
            self.issaving = False
            return

        text, ok = QInputDialog.getText(self, '输入姓名', '输入名称:')

        if ok:
            self.tmpname = text
            print('self.tmpname', self.tmpname)
        else:
            self.issaving = False
            return

        # 从label获取名和曾

        # filename = os.getcwd()
        print('tmpname', self.tmpname)
        print(os.getcwd() + '\\Photos\\')

        filename = os.getcwd() + '\\Photos\\' + str(self.num) + '.' + self.tmpname
        print('filename', filename)

        ddd = filename + '.jpg'

        print(ddd)

        if self.showImage == None:
            print('进入')

            # 复制图片
            # if self.tmpfilename == ddd or self.tmp.peohasbeensaved():
            if self.tmpfilename == ddd:
                QMessageBox.warning(self, '警告', '图片已存在')
                self.issaving = False
                self.tmp.config_is_right()
                return

            print('进入2')
            print('self.tmpname', self.tmpname)
            print('self.tmpfilename', self.tmpfilename)
            shutil.copy(self.tmpfilename, ddd)

            print('tmpname', self.tmpname)

            print('ddd', ddd)
            self.hadsave = True
            self.allowdiscern = False
            self.needtrain = True
            self.tmp.config_is_right()

            self.num = self.tmp.getConf_num() + 1

            self.selectnum = [str(i) for i in range(1, self.num)]
            self.filenum = [os.path.split(os.path.join(self.photodir_path, f))[1].split('.')[0] for f in
                            os.listdir(self.photodir_path)]
            self.selectnum = list(set(self.selectnum) - set(self.filenum))

            self.issaving = False
            return

        self.showImage.save(ddd, "JPG", 100)
        self.hadsave = True
        self.allowdiscern = False
        self.needtrain = True
        self.tmp.config_is_right()

        self.num = self.tmp.getConf_num() + 1

        self.selectnum = [str(i) for i in range(1, self.num+1)]
        self.filenum = [os.path.split(os.path.join(self.photodir_path, f))[1].split('.')[0] for f in
                        os.listdir(self.photodir_path)]
        self.selectnum = list(set(self.selectnum) - set(self.filenum))

        self.issaving = False
        # 拍照

    def capx(self):
        self.issaving = True
        self.hadsave = False

        if not self.timer_camera.isActive():
            QMessageBox.warning(self, '警告', '没有打开摄像头')
            return

        # 显示showImage的图片
        self.cap_label.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
        self.right_exist = True
        # 允许保存
        self.allowsave = True

    # 关闭事件
    def closeEvent(self, event):
        self.tmp.config_is_right()
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')

        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            # self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())
