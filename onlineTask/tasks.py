import json
import os
import shutil
import time
from ftplib import FTP

import numpy as np
from ModelToSQL.celery import app
from multiprocessing import Process, Event, Queue
import cv2
from ModelToSQL.settings import BASE_DIR
from compare.image_compare_multiprocess import compare_handle
from image_compare import get_gps
from onlineTask.models import OnlineTask, OnlineImageIdentifyInfo
from splice.image_stitch_multiprocess import splice_handle
from preprocess.image_preprocess import preprocess_handle
from offlineTask.models import OfflineTask, OfflinePreprocessSet, SingleImageSpliceInfo
from splice.apps import seam_process, transform_process
import splice.image_stitch as ist
import preprocess.image_preprocess as ipp
from PIL import Image
from yolo import YOLO
import socket
import struct
import demjson


class MyFtp:
    ftp = FTP()

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)

    def login(self, username, pwd):
        self.ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        self.ftp.login(username, pwd)
        print(self.ftp.welcome)

    def downloadFile(self, localpath, remotepath, filename):
        os.chdir(localpath)  # 切换工作路径到下载目录
        self.ftp.cwd(remotepath)  # 要登录的ftp目录
        self.ftp.nlst()  # 获取目录下的文件
        # file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
        # self.ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handle, blocksize=1024)  # 下载ftp文件
        # # ftp.delete（filename）  # 删除ftp服务器上的文件
        try:
            print('>>>>>>>>>>>>下载文件 %s ... ...' % filename)
            buf_size = 10240
            file_handler = open(filename, 'wb')
            self.ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handler.write, buf_size)
            file_handler.close()
        except Exception as err:
            print('下载文件出错，出现异常：%s ' % err)
            return

    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()


def saveOnlineIdentify(userId, userOverdate, imageIdentifyPath, onlineIdentifyPreId):
    onlineImageIdentifyInfo = OnlineImageIdentifyInfo.objects.get(id=onlineIdentifyPreId)
    user = OnlineTask.objects.get(id=userId)
    onlineImageIdentifyInfo.imageIdentifyPath = imageIdentifyPath
    onlineImageIdentifyInfo.is_identify = True
    onlineImageIdentifyInfo.save()

    onlineImageIdentifyInfos = OnlineImageIdentifyInfo.objects.all()
    taskFlag = False
    for onlineImageIdentifyInfo in onlineImageIdentifyInfos:
        print(user.task_status, onlineImageIdentifyInfo.overDate, onlineImageIdentifyInfo.is_identify)
        if onlineImageIdentifyInfo.overDate == userOverdate and onlineImageIdentifyInfo.is_identify == False:
            taskFlag = True
            break

    if not taskFlag and user.task_status == 'd':
        user.identify_status = 'd'
        user.save()
        return False

    return True


def saveOnlinePreprocess(imagePreprocessPath, onlineIdentifyPreId):
    onlineImageIdentifyInfo = OnlineImageIdentifyInfo.objects.get(id=onlineIdentifyPreId)

    onlineImageIdentifyInfo.imagePreprocessPath = imagePreprocessPath
    onlineImageIdentifyInfo.save()


def copyImageToFile(userOverdate, userTitle, fileName, origin_folder):
    time.sleep(2)
    try:
        shutil.copy("D:/202006115wjk/QtFtp/" + fileName, origin_folder + fileName)
    except Exception as e:
        print(fileName + "not ready!!!!")
        return
    onlineImageIdentifyInfo = OnlineImageIdentifyInfo()
    onlineImageIdentifyInfo.is_identify = False
    onlineImageIdentifyInfo.is_show = False
    onlineImageIdentifyInfo.imageOriginPath = origin_folder + fileName
    onlineImageIdentifyInfo.title = userTitle
    onlineImageIdentifyInfo.overDate = userOverdate
    onlineImageIdentifyInfo.save()

    return onlineImageIdentifyInfo.id


class online_enhance_process(Process):
    def __init__(self, name, userId, userOverdate, userTitle, enhancedQ, save_path, isIdentifyPre, is_gamma=False, is_clahe=False):
        Process.__init__(self)
        self.name = name
        self.userId = userId
        self.enhancedQ = enhancedQ
        self.save_path = save_path
        self.isIdentifyPre = isIdentifyPre
        self.is_gamma = is_gamma
        self.is_clahe = is_clahe
        self.userOverdate = userOverdate
        self.userTitle = userTitle

    def run(self):
        print("Starting " + self.name + " Process")
        while True:
            users = OnlineTask.objects.get(id=self.userId)
            onlineImages = OnlineImageIdentifyInfo.objects.all()
            identifyFlag = False
            for onlineImage in onlineImages:
                #print('======='+ str(onlineImage.id) + '=======' + onlineImage.overDate + '======= b%' + onlineImage.is_identify)
                if onlineImage.overDate == self.userOverdate and onlineImage.is_identify == False:
                    identifyFlag = True
                    #img_path, progress, onlineIdentifyPreId = self.loadedQ.get()
                    enhanced_img = cv2.imdecode(np.fromfile(onlineImage.imageOriginPath, dtype=np.uint8), 1)
                    if self.isIdentifyPre:
                        users.preprocess_status='p'
                        users.save()
                        if self.is_gamma:
                            enhanced_img = ipp.gamma_trans(enhanced_img, gamma=0.5)
                        if self.is_clahe:
                            enhanced_img = ipp.hist_equal_CLAHE(enhanced_img, clipLimit=1.0, tileGridSize=(9, 9))
                    img_name = os.path.basename(onlineImage.imageOriginPath)
                    # gps_info = get_gps(img_path)
                    if not os.path.exists(self.save_path):
                        os.makedirs(self.save_path)
                    # cv2.imwrite(save_path + img_name, loaded_img)
                    cv2.imencode('.jpg', enhanced_img)[1].tofile(self.save_path + img_name)
                    # cv2.imwrite(self.save_path + img_name, enhanced_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    ipp.copy_img_exif(onlineImage.imageOriginPath, self.save_path + img_name)
                    self.enhancedQ.put((enhanced_img, self.save_path + img_name, onlineImage.id))
                    saveOnlinePreprocess(self.save_path + img_name, onlineImage.id)
                    print("enhanced image: " + img_name, "task_status：" + users.task_status)
            if identifyFlag == False and users.task_status == 'd':
                users.preprocess_status = 'd'
                users.save()
                print("online_enhance_process end")
                break


class online_identify_process(Process):
    def __init__(self, name, userId, userOverdate, userTitle, enhancedQ, save_path):
        Process.__init__(self)
        self.name = name
        self.userId = userId
        self.userOverdate = userOverdate
        self.userTitle = userTitle
        self.enhancedQ = enhancedQ
        self.save_path = save_path

    def run(self):
        print("Starting " + self.name + " Process")
        yolo = YOLO()
        users = OnlineTask.objects.get(id=self.userId)
        while True:
            users.identify_status='p'
            users.save()
            enhanced_img, img_path, onlineIdentifyPreId = self.enhancedQ.get()

            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)

            img_name = os.path.basename(img_path)
            img = Image.open(img_path)
            r_image = yolo.detect_image(img)
            rawimg = np.array(r_image)
            cv2.imencode('.jpg', rawimg)[1].tofile(self.save_path + img_name)
            taskFlag = saveOnlineIdentify(self.userId, self.userOverdate, self.save_path + img_name, onlineIdentifyPreId)
            print("detect_image image: " + img_name)
            if not taskFlag:
                users.identify_status='d'
                users.preprocess_status = 'd'
                users.save()
                print("online_enhance_identify_process end")
                break


def online_handle_queue(userId, origin_folder, overDate, mapNickName, isIdentifyPre, is_gamma, is_clahe):
    print("start online_handle_queue Process")
    enhancedQ = Queue(4)
    suffix = ".JPG"

    processes = []
    process_ep = online_enhance_process("Image_Enhance", userId, overDate, mapNickName, enhancedQ, origin_folder.replace('origin', 'preprocess'), isIdentifyPre, is_gamma, is_clahe)
    process_ep.start()
    processes.append(process_ep)
    process_id = online_identify_process("Image_Identify", userId, overDate, mapNickName, enhancedQ, origin_folder.replace('origin', 'identify'))
    process_id.start()
    processes.append(process_id)

    # for p in processes:
    #     p.join()
    #
    # enhancedQ.close()
    print("Exitting onlinemosiac_handle Process")


class socketTask(Process):
    def __init__(self, name, messageQ, ip, port, queryset, userId, overDate, mapNickName, origin_folder):
        Process.__init__(self)
        self.name = name
        self.messageQ = messageQ
        self.ip = ip
        self.port = port
        self.queryset = queryset
        self.userId = userId
        self.overDate = overDate
        self.mapNickName = mapNickName
        self.origin_folder = origin_folder

    def run(self):
        print("Starting " + self.name + " OnlineProcess")
        ftp = MyFtp('127.0.0.1')
        ftp.login('admin', 'admin')
        try:
            client = socket.socket()
            client.connect((self.ip, self.port))
            while True:
                data = client.recv(1024, socket.MSG_WAITALL)
                #client.send('000'.encode("utf-8"))4
                #print(data.decode('gbk'))
                #receiveJson = json.loads(data.decode())
                receiveJson = json.loads(str(data)[str(data).index('{'):str(data).index('}')+1])
                if 'MissionStatus' in receiveJson:
                    if receiveJson['MissionStatus'] == 1:
                        self.queryset.update(task_status='p')
                    elif receiveJson['MissionStatus'] == 0:
                        self.queryset.update(task_status='d')
                        break
                elif 'PictureNo' in receiveJson:
                    # try:
                    #     ftp.downloadFile(self.origin_folder, '/', receiveJson['PictureNo'])
                    # except Exception as e:
                    #     print(receiveJson['PictureNo'])
                    copyImageToFile(self.overDate, self.mapNickName, receiveJson['PictureNo'], self.origin_folder)
        except ConnectionError as ex:
            print(ex)


def onlinemosiac_handle(userId, queryset):
    ip = '127.0.0.1'
    port = 8888
    messageQ = Queue(5)
    user = OnlineTask.objects.get(id=userId)
    print(user.id, user.overDate)
    origin_folder = '%s/%s/%s/%s/%s/' % (
        BASE_DIR.replace('\\', '/'), 'static/upload/onlineTask', user.title.mapNickName, user.overDate,'origin')
    if not os.path.exists(origin_folder):
        os.makedirs(origin_folder)

    #shutil.copy(load_path + fileName, origin_folder + fileName)
    process_rc = socketTask("socket_Task", messageQ, ip, port, queryset, userId,  user.overDate, user.title.mapNickName, origin_folder)
    process_rc.start()

    online_handle_queue(userId, origin_folder, user.overDate, user.title.mapNickName, user.isIdentifyPre, user.preprocessSet.is_gamma, user.preprocessSet.is_clahe)


