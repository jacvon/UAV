import preprocess.image_enhance as ieh
import preprocess.image_dehaze as idh
import splice.image_mosiac as ims
from multiprocessing import freeze_support, cpu_count
from multiprocessing import Process, Event, Queue
import os
import cv2
import numpy as np
import time


class load_process(Process):
    def __init__(self, name, numQ, loadedQ, num_evt, read_path, suffix, is_dehaze):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.num_evt = num_evt
        self.read_path = read_path
        self.suffix = suffix
        self.is_dehaze = is_dehaze

    def run(self):
        print("Starting " + self.name + " Process")
        img_files, img_names = ims.getImgList(self.read_path, self.suffix, reverse=False)
        next_stage_num = 3
        for i in range(next_stage_num):
            self.numQ.put(len(img_files))
        self.num_evt.set()
        for index, file in enumerate(img_files):
            loaded_img = cv2.imread(file)
            if self.is_dehaze:
                loaded_img = idh.dehaze(loaded_img, sz=9, bGamma=False)
            self.loadedQ.put([loaded_img, img_names[index]])
            print("loaded image: " + img_names[index])
        print("Exitting " + self.name + " Process")


class enhance_process(Process):
    def __init__(self, name, numQ, loadedQ, enhancedQ, num_evt, save_path):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.enhancedQ = enhancedQ
        self.num_evt = num_evt
        self.save_path = save_path

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        count = 0
        while count < img_num:
            recv_data = self.loadedQ.get()
            enhanced_img = ieh.gamma_trans(recv_data[0], gamma=0.5)
            enhanced_img = ieh.hist_equal_CLAHE(enhanced_img, clipLimit=1.0, tileGridSize=(9, 9))
            self.enhancedQ.put([enhanced_img, recv_data[1]])
            cv2.imwrite(self.save_path + recv_data[1], enhanced_img)
            count += 1
            print("enhanced image : " + recv_data[1])
        print("Exitting " + self.name + " Process")
