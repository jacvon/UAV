from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from multiprocessing import freeze_support, cpu_count
from multiprocessing import Process, Event, Queue
import os
import cv2
import numpy as np
import time

from preprocess.apps import load_process, enhance_process
from splice.apps import seam_process, transform_process


class MyAppConfig(AppConfig):
    name = 'offlineTask'
    verbose_name = _("图像离线处理")


def begin_handle(path):
    print('CPU核心数量:' + str(cpu_count()))
    freeze_support()
    numQ = Queue(3)
    loadedQ = Queue(4)
    enhancedQ = Queue(4)
    transformedQ = Queue(4)
    num_evt = Event()

    read_path = path
    enhance_save_path = "../CV2_LEARN/Aerial_Images/New_Image_Set/"
    merge_save_path = "../CV2_LEARN/Aerial_Images/Merge_Result/"
    suffix = ".JPG"
    is_dehaze = True
    is_each_save = True

    processes = []
    process_lp = load_process("Image_Load", numQ, loadedQ, num_evt, read_path, suffix, is_dehaze)
    process_ep = enhance_process("Image_Enhance", numQ, loadedQ, enhancedQ, num_evt, enhance_save_path)

    process_tp = transform_process("Image_Transform", numQ, enhancedQ, transformedQ, num_evt)
    process_sp = seam_process("Image_Beam", numQ, transformedQ, num_evt, merge_save_path, suffix, is_each_save)

    processes.append(process_lp)
    processes.append(process_ep)
    processes.append(process_tp)
    processes.append(process_sp)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    numQ.close()
    loadedQ.close()
    enhancedQ.close()
    transformedQ.close()
    print("Exitting Main Process")