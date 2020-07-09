import os
import shutil
import time
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
from yolo import YOLO, detect_video

def saveOnlineIdentify(userOverdate, userTitle, imageIdentifyPath, onlineIdentifyPreId):
    onlineImageIdentifyInfos = OnlineImageIdentifyInfo.objects.all()
    for onlineImageIdentifyInfo in onlineImageIdentifyInfos:
        if onlineImageIdentifyInfo.id == onlineIdentifyPreId:
            onlineImageIdentifyInfo.imageIdentifyPath = imageIdentifyPath
            onlineImageIdentifyInfo.save()
            break

def saveOnlinePreprocess(userOverDate, userTitle, imagePreprocessPath, onlineIdentifyPreId):
    onlineImageIdentifyInfos = OnlineImageIdentifyInfo.objects.all()
    for onlineImageIdentifyInfo in onlineImageIdentifyInfos:
        if onlineImageIdentifyInfo.id == onlineIdentifyPreId:
            onlineImageIdentifyInfo.imagePreprocessPath = imagePreprocessPath
            onlineImageIdentifyInfo.save()
            break

def copyImageToFile(userOverdate, userTitle, img_path, img_name, progress, origin_folder):

    if not os.path.exists(origin_folder):
        os.makedirs(origin_folder)

    shutil.copy(img_path, origin_folder + img_name)

    onlineImageIdentifyInfo = OnlineImageIdentifyInfo()
    onlineImageIdentifyInfo.is_identify=False
    onlineImageIdentifyInfo.is_show=False
    onlineImageIdentifyInfo.imageOriginPath = origin_folder + img_name
    onlineImageIdentifyInfo.title=userTitle
    onlineImageIdentifyInfo.overDate=userOverdate
    onlineImageIdentifyInfo.progress = progress
    onlineImageIdentifyInfo.save()

    return onlineImageIdentifyInfo.id

class receive_process(Process):
    def __init__(self, name, userOverdate, userTitle, loadedQ, load_path, save_path, suffix=".jpg"):
        Process.__init__(self)
        self.name = name
        self.loadedQ = loadedQ
        self.load_path = load_path
        self.save_path = save_path
        self.suffix = suffix
        self.userOverdate = userOverdate
        self.userTitle = userTitle

    def run(self):
        print("Starting " + self.name + " Process")
        img_paths, img_names = ist.getImgList(self.load_path, self.suffix, reverse=True)
        progress = True
        index = 0
        while index<5:
            onlineIdentifyPreId = copyImageToFile(self.userOverdate, self.userTitle, img_paths[index], img_names[index], progress, self.save_path)
            self.loadedQ.put((self.save_path + img_names[index], progress, onlineIdentifyPreId))
            index += 1
            time.sleep(3)
        print("Exitting " + self.name + " Process")

class online_enhance_process(Process):
    def __init__(self, name, queryset, userOverdate, userTitle, loadedQ, enhancedQ, save_path, isIdentifyPre, is_gamma=False, is_clahe=False):
        Process.__init__(self)
        self.name = name
        self.loadedQ = loadedQ
        self.enhancedQ = enhancedQ
        self.save_path = save_path
        self.isIdentifyPre = isIdentifyPre
        self.is_gamma = is_gamma
        self.is_clahe = is_clahe
        self.userOverdate = userOverdate
        self.userTitle = userTitle
        self.queryset = queryset


    def run(self):
        print("Starting " + self.name + " Process")

        while True:
            img_path, progress, onlineIdentifyPreId = self.loadedQ.get()
            enhanced_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            if self.isIdentifyPre:
                self.queryset.update(preprocess_status='p')
                if self.is_gamma:
                    enhanced_img = ipp.gamma_trans(enhanced_img, gamma=0.5)
                if self.is_clahe:
                    enhanced_img = ipp.hist_equal_CLAHE(enhanced_img, clipLimit=1.0, tileGridSize=(9, 9))
            img_name = os.path.basename(img_path)
            #gps_info = get_gps(img_path)
            self.enhancedQ.put((enhanced_img, progress, onlineIdentifyPreId,img_path))
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            #cv2.imwrite(save_path + img_name, loaded_img)
            cv2.imencode('.jpg', enhanced_img)[1].tofile(self.save_path + img_name)
            #cv2.imwrite(self.save_path + img_name, enhanced_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            ipp.copy_img_exif(img_path, self.save_path + img_name)
            saveOnlinePreprocess(self.userOverdate, self.userTitle, self.save_path + img_name, onlineIdentifyPreId)
            print("enhanced image: " + img_name)
            if progress is False:
                self.queryset.update(preprocess_status='d')
                break
        print("Exitting " + self.name + " Process")

class online_identify_process(Process):
    def __init__(self, name, queryset, userOverdate, userTitle, enhancedQ, save_path):
        Process.__init__(self)
        self.name = name
        self.queryset = queryset
        self.userOverdate = userOverdate
        self.userTitle = userTitle
        self.enhancedQ = enhancedQ
        self.save_path = save_path

    def run(self):
        print("Starting " + self.name + " Process")
        yolo = YOLO()
        while True:
            self.queryset.update(identify_status='p')
            enhanced_img, progress, onlineIdentifyPreId,img_path = self.enhancedQ.get()

            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)

            img_name = os.path.basename(img_path)
            img = Image.open(img_path)
            r_image = yolo.detect_image(img)
            rawimg = np.array(r_image)
            cv2.imencode('.jpg', rawimg)[1].tofile(self.save_path + img_name)
            saveOnlineIdentify(self.userOverdate, self.userTitle, self.save_path + img_name, onlineIdentifyPreId)
            print("enhanced image: " + img_name)
            if progress is False:
                self.queryset.update(preprocess_status='d')
                break
        print("Exitting " + self.name + " Process")

def onlinemosiac_handle(userId, queryset):
    print("start onlineMosiac Process")
    loadedQ = Queue(4)
    enhancedQ = Queue(4)
    load_path = "D:/202006115wjk/原始图片/"
    suffix = ".JPG"

    users = OnlineTask.objects.all()
    for user in users:
        if user.id == userId:
            origin_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR.replace('\\', '/'), 'static/upload/onlineTask', user.title.mapNickName, user.overDate, 'origin')
            processes = []
            process_re = receive_process("receive_Load", user.overDate, user.title.mapNickName, loadedQ, load_path, origin_folder, suffix)
            process_re.start()
            processes.append(process_re)
            process_ep = online_enhance_process("Image_Enhance", queryset, user.overDate, user.title.mapNickName, loadedQ, enhancedQ, origin_folder.replace('origin','preprocess'),
                                         user.isIdentifyPre, user.preprocessSet.is_gamma, user.preprocessSet.is_clahe)
            process_ep.start()
            processes.append(process_ep)
            process_id = online_identify_process("Image_Identify", queryset, user.overDate, user.title.mapNickName, enhancedQ, origin_folder.replace('origin', 'identify'))
            process_id.start()
            processes.append(process_id)
        print("Exitting onlinemosiac_handle Process")