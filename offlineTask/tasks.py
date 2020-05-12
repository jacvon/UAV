from multiprocessing.process import current_process

from ModelToSQL.celery import app
import os
import shutil

from ModelToSQL.settings import BASE_DIR
from App.detect_project.predict_my import func_predict
from offlineTask.models import SingleImageInfo, SingleImageIdentifyInfo
from multiprocessing import freeze_support, cpu_count
from multiprocessing import Process, Event, Queue
import os
import cv2
import numpy as np
import time

from ModelToSQL.settings import BASE_DIR
from preprocess.apps import load_process, enhance_process
from splice.apps import seam_process, transform_process

@app.task(name='offlineTask.tasks.begin_handle')
def begin_handle(path):
    current_process()._config = {'semprefix': '/mp'}
    print('CPU核心数量:' + str(cpu_count()))
    print('原始图片路径'+ path)
    freeze_support()
    numQ = Queue(3)
    loadedQ = Queue(4)
    enhancedQ = Queue(4)
    transformedQ = Queue(4)
    num_evt = Event()

    read_path = BASE_DIR + "/static/upload/" +path
    enhance_save_path = read_path.replace('origin','preprocess')
    merge_save_path = read_path.replace('origin','splice')
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
