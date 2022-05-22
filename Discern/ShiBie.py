import cv2
# import numpy as np
import os

import CV2AddChinese as AddCh


class ShiBieObject:
    def __init__(self):
        # 加载训练数据集文件

        self.trainpath = './Trainer/trainer.yml'
        if not os.path.exists(self.trainpath):
            print('文件不存在先训练')
            return



        self.recogizer = cv2.face.LBPHFaceRecognizer_create()
        self.recogizer.read('./Trainer/trainer.yml')
        self.names = []
        self.warningtime = 0

        nameaa = os.listdir('./Photos/')

        i = 0
        for im in nameaa:
            nam = im.split('.')[1]

            i += 2
            self.names.append(nam)
        print('self.names', self.names)

    # 准备识别的图片
    def face_detect_demo(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
        face_detector = cv2.CascadeClassifier('../Lib/haarcascade_frontalface_alt2.xml')
        face = face_detector.detectMultiScale(gray, 1.07, 5, cv2.CASCADE_SCALE_IMAGE)

        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
            cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)

            # 人脸识别
            id, confidence = self.recogizer.predict(gray[y:y + h, x:x + w])

            print('标签id:', id, '置信评分：', confidence)

            if confidence > 80:
                img = AddCh.cv2AddChinese(img, '未识别', (x + 10, y - 10), (0, 255, 0), 30)
                #cv2.putText(img, '未识别', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)

            else:
                img = AddCh.cv2AddChinese(img, str(self.names[id - 1]), (x + 20, y - 10), (0, 255, 0), 30)

        cv2.imshow('Result', img)

    def run(self):

        cap = cv2.VideoCapture(0)

        while True:

            flag, frame = cap.read()

            if not flag:
                break
            self.face_detect_demo(frame)

            if ord(' ') == cv2.waitKey(10):
                break

        cv2.destroyAllWindows()
        cap.release()

# a = ShiBieObject()
# a.run()
