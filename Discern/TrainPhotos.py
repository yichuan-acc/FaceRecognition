import os
import cv2
from PIL import Image
import numpy as np
from TakePhotos import TakeP


class Tra:

    def __init__(self):
        # 保存文件
        if not os.path.exists('./Trainer/'):
            os.mkdir('./Trainer/')

        self.trainpath = './Trainer/trainer.yml'

        # self.names = {}
        self.path = os.getcwd() + '\\Photos\\'
        self.files = os.listdir(self.path)
        self.Takpp = TakeP()

    def getImageAndLabels(self):
        path = self.path

        self.Takpp.config_is_right()
        # 存储人脸数据
        facesSamples = []
        # 存储编号数据
        ids = []
        # 存储图片信息
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        print(imagePaths)

        # 加载分类器
        face_detector = cv2.CascadeClassifier('../Lib/haarcascade_frontalface_alt2.xml')
        # 打印数组imagePaths

        # 遍历列表中的图片
        for imagePath in imagePaths:
            # 打开图片，灰度化 PIL
            PIL_img = Image.open(imagePath).convert('L')

            img_numpy = np.array(PIL_img, 'uint8')
            # 获取图片人脸特征
            faces = face_detector.detectMultiScale(img_numpy)

            # 获取每张图片的人脸特征
            did = int(os.path.split(imagePath)[1].split('.')[0])
            print('pathid', did)

            # 预防无面容照片
            for x, y, w, h in faces:
                ids.append(did)
                print('did', did)
                facesSamples.append(img_numpy[y:y + h, x:x + w])

        return facesSamples, ids

    def run(self):

        from TakePhotos import TakeP

        tmp = TakeP()
        tmp.config_is_right()

        # 获取图像数组和id标签组和姓名
        faces, ids = self.getImageAndLabels()
        print(ids)
        print(faces)
        # 加载识别器
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        # 训练
        recognizer.train(faces, np.array(ids))
        recognizer.write('./Trainer/trainer.yml')

# a = Tra()
# a.run()
