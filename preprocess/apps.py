import pyexiv2
import preprocess.image_preprocess as ipp
import preprocess.image_dehaze as idh
import splice.image_mosiac as ims
from multiprocessing import Process, Event, Queue
import os
import cv2
import numpy as np
from PIL import Image


class load_process(Process):
    def __init__(self, name, numQ, loadedQ, num_evt, load_path, suffix=".jpg", is_brightness = True, is_dehaze=False):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.num_evt = num_evt
        self.load_path = load_path
        self.suffix = suffix
        self.is_brightness = is_brightness
        self.is_dehaze = is_dehaze

    def run(self):
        global brightness_avg
        print("Starting " + self.name + " Process")
        img_paths, img_names = ims.getImgList(self.load_path, self.suffix)
        if self.is_brightness:
            brightness_avg = ipp.get_avg_brightness(img_paths)
        next_stage_num = 3
        for i in range(next_stage_num):
            self.numQ.put(len(img_paths))
        self.num_evt.set()
        for index, img_path in enumerate(img_paths):
            #loaded_img = cv2.imread(img_path)
            loaded_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            if self.is_dehaze:
                loaded_img = idh.dehaze(loaded_img, size=9, bGamma=False)
            if self.is_brightness:
                pil_img = Image.fromarray(cv2.cvtColor(loaded_img,cv2.COLOR_BGR2RGB))
                pil_img = ipp.set_brightness(pil_img, brightness_avg)
                loaded_img = np.asarray(pil_img)
            loaded_img = cv2.cvtColor(loaded_img, cv2.COLOR_RGB2BGR)
            self.loadedQ.put((loaded_img, img_path))
            print("loaded image: " + img_names[index])
        print("Exitting " + self.name + " Process")


class enhance_process(Process):
    def __init__(self, name, useId, numQ, loadedQ, enhancedQ, num_evt, save_path, is_gamma=False, is_clahe=False):
        Process.__init__(self)
        self.useId = useId
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.enhancedQ = enhancedQ
        self.num_evt = num_evt
        self.save_path = save_path
        self.is_gamma = is_gamma
        self.is_clahe = is_clahe

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        count = 0
        while count < img_num:
            enhanced_img, img_path = self.loadedQ.get()
            if self.is_gamma:
                enhanced_img = ipp.gamma_trans(enhanced_img, gamma=0.5)
            if self.is_clahe:
                enhanced_img = ipp.hist_equal_CLAHE(enhanced_img, clipLimit=1.0, tileGridSize=(9, 9))
            img_name = os.path.basename(img_path)
            gps_info = get_gps(img_path)
            self.enhancedQ.put((enhanced_img, img_name, gps_info))
            #cv2.imwrite(self.save_path + img_name, enhanced_img)
            cv2.imencode('.jpg', enhanced_img)[1].tofile(self.save_path + img_name)
            copy_img_exif(img_path, self.save_path + img_name)
            count += 1
            print("enhanced image : " + img_name)
        print("Exitting " + self.name + " Process")


def get_gps(file):
    def convert_gps(coord_arr):
        arr = str(coord_arr).replace('[', '').replace(']', '').replace('\'', '').split(', ')
        d = float(arr[0].split('/')[0]) / float(arr[0].split('/')[1])
        m = float(arr[1].split('/')[0]) / float(arr[1].split('/')[1])
        s = float(arr[2].split('/')[0]) / float(arr[2].split('/')[1])
        return float(d) + (float(m) / 60) + (float(s) / 3600)

    try:
        exif_dict = pyexiv2.Image(file, encoding='gbk').read_exif()
        long = exif_dict.get("Exif.GPSInfo.GPSLongitude").split()
        long = convert_gps(long)
        lat = exif_dict.get("Exif.GPSInfo.GPSLatitude").split()
        lat = convert_gps(lat)
        alt = exif_dict.get("Exif.GPSInfo.GPSAltitude")
        alt = float(alt.split('/')[0]) / float(alt.split('/')[1])
    except Exception as e:
        print("ERROR:", e)
        print("请确保图像文件" + file + "包含经纬度等EXIF有效信息！")
        return None
    else:
        return np.float64([long, lat, alt]).reshape(1, 3)


def copy_img_exif(src_file, dest_file):
    try:
        src_img = pyexiv2.Image(src_file, encoding='gbk')
        dest_img = pyexiv2.Image(dest_file, encoding='gbk')
        # dest_img.modify_exif(src_img.read_exif())
        dest_img.modify_exif({"Exif.GPSInfo.GPSLongitude": src_img.read_exif().get("Exif.GPSInfo.GPSLongitude")})
        dest_img.modify_exif({"Exif.GPSInfo.GPSLatitude": src_img.read_exif().get("Exif.GPSInfo.GPSLatitude")})
        dest_img.modify_exif({"Exif.GPSInfo.GPSAltitude": src_img.read_exif().get("Exif.GPSInfo.GPSAltitude")})
    except Exception as e:
        print("ERROR:", e)
        print("图像文件" + dest_file + "的EXIF属性修改操作失败！")