import cv2
import os
import configparser


class TakeP:

    def __init__(self, ):

        self.config_path = os.getcwd() + '\\config.ini'
        self.photodir_path = os.getcwd() + '\\Photos\\'
        self.recogizer = cv2.face.LBPHFaceRecognizer_create()
        self.recogizer.read('./Trainer/trainer.yml')

        self.conform_and_create_path(self.photodir_path)
        self.conform_and_create_path(self.config_path)
        self.config_is_right()

        self.names = [os.path.split(os.path.join(self.photodir_path, f))[1].split('.')[1] for f in
                      os.listdir(self.photodir_path)]

        print('self.names', self.names)

        self.num = 0

    # 验证并且创建文件或文件夹
    def conform_and_create_path(self, path):
        # 存在这个文件夹或路径
        if os.path.exists(path):
            pass

        # 不存在并且是路径
        elif os.path.isdir(path):
            # 创建
            os.mkdir(path)

        # 不存在并且是文件
        else:
            # 创建
            file = open(path, 'w')

            conf = {
                'numbers': str(0)
            }

            # 写入配置文件
            self.writeConf(conf)
            file.close()

    # 验证配置文件
    def config_is_right(self):

        nums = self.getConf_num()
        files = os.listdir(os.path.abspath(self.photodir_path))
        pathnums = len(files)
        if nums == pathnums:
            print('正确')
        else:
            conf = {
                'numbers': str(pathnums)
            }

            # 写入配置文件
            self.writeConf(conf)

    # 传入一个字典类型
    def writeConf(self, conf):
        config = configparser.ConfigParser()
        config['DEFAULT'] = conf
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
            print('已更新配置文件')

    # 获得已有的人数
    def getConf_num(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        num = int(config.get('DEFAULT', 'numbers'))
        return num

    # 传入照片的姓名
    def getPhoto(self, peoplename):

        # 当前保存的序号
        self.num = self.getConf_num() + 1

        # 打开摄像头
        cap = cv2.VideoCapture(0)

        self.config_is_right()

        path = self.photodir_path

        # 确定路径存在
        self.conform_and_create_path(os.path.abspath(path))

        while cap.isOpened():
            ret_flag, Vshow = cap.read()  # 保存每帧图像
            cv2.imshow('Capture_Test', Vshow)

            k = cv2.waitKey(1) & 0xFF

            # 需要GUI事件绑定
            key = 's'
            if k == ord(key):
                # 此函数能保存中文文件名
                # imgpath = path + str(num) + '.' + peoplename + ".jpg"
                imgpath = path + str(self.num) + '.' + peoplename + ".jpg"

                print('names', self.names)

                name = peoplename

                if (name in self.names) or self.peohasbeensaved(Vshow):
                    print('重复')
                    print('你要覆盖原来的照片吗?')
                    print(self.num)
                    print('name', name)
                    print('几个', self.peohasbeensaved(Vshow))

                else:
                    # 保存
                    cv2.imencode('.jpg', Vshow)[1].tofile(imgpath)
            elif k == ord(' '):
                self.config_is_right()
                break

        # 释放摄像头
        cap.release()

        # 释放内存
        cv2.destroyAllWindows()

    def peohasbeensaved(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
        face_detector = cv2.CascadeClassifier('../Lib/haarcascade_frontalface_alt2.xml')

        face = face_detector.detectMultiScale(gray, 1.07, 5, cv2.CASCADE_SCALE_IMAGE)

        for x, y, w, h in face:

            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
            cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)

            # 人脸识别
            id, confidence = self.recogizer.predict(gray[y:y + h, x:x + w])

            # print('标签id:',ids,'置信评分：', confidence)
            if confidence > 80:

                return False

            else:
                # img = AddCh.cv2AddChinese(img, tmpname, (x + 20, y - 10), (0, 255, 0), 30)
                # 识别成功已存在
                return True

        # cv2.imshow('result', img)
