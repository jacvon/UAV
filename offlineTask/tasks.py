import os
from ModelToSQL.celery import app
from compare.image_comparison import single_compare_process, getImgList
from multiprocessing import Process, Event, Queue
import cv2
from ModelToSQL.settings import BASE_DIR
from preprocess.apps import load_process, enhance_process
from splice.apps import seam_process, transform_process

#@app.task(name='offlineTask.tasks.mosiac_handle')
def   mosiac_handle(originPath, userOverdate, userTitleId):
    print("start Mosiac Process")
    numQ = Queue(3)
    loadedQ = Queue(4)
    enhancedQ = Queue(4)
    transformedQ = Queue(4)
    num_evt = Event()

    load_path = BASE_DIR.replace('\\','/') + "/static/upload/" + originPath

    enhance_save_path = load_path.replace('origin','preprocess')

    if not os.path.exists(enhance_save_path):
        os.makedirs(enhance_save_path)

    merge_save_path = load_path.replace('origin','splice')

    if not os.path.exists(merge_save_path):
        os.makedirs(merge_save_path)
    suffix = ".JPG"
    is_brightness = True  # 一般有必要对所有待拼接图进行亮度均衡
    is_dehaze = False  # 若图像无雾使用会使图像变暗
    is_gamma = True  # 在图像偏亮或偏暗时用于校正
    is_clahe = True  # 若需增强图像对比度可进行直方图均衡化
    is_each_save = True  # 保存每一步拼接过程的中间结果

    processes = []
    process_lp = load_process("Image_Load", numQ, loadedQ, num_evt, load_path, suffix, is_brightness, is_dehaze)
    process_lp.start()
    processes.append(process_lp)
    process_ep = enhance_process("Image_Enhance",userOverdate, userTitleId,numQ, loadedQ, enhancedQ, num_evt, enhance_save_path, is_gamma,
                                 is_clahe)
    process_ep.start()
    processes.append(process_ep)
    process_tp = transform_process("Image_Transform", numQ, enhancedQ, transformedQ, num_evt)
    process_tp.start()
    processes.append(process_tp)
    process_sp = seam_process("Image_Beam",userOverdate, userTitleId,numQ, transformedQ, num_evt, merge_save_path, suffix, is_each_save)
    process_sp.start()
    processes.append(process_sp)

    """
    for p in processes:
        p.join()

    numQ.close()
    loadedQ.close()
    enhancedQ.close()
    transformedQ.close()
    """
    print("Exitting Mosiac Process")

@app.task(name='offlineTask.tasks.compare_handle')
def compare_handle(userId, pathImage, pathCsv):
    input_path = ''
    PROCESS_NUM = 4
    output_path = input_path.replace('preprocess','compare')
    suffix = ".JPG"

    origImg = cv2.imread(pathImage)
    csv_file = pathCsv

    compImg_files, compImg_names = getImgList(input_path, suffix, reverse=False)
    compImg_num = len(compImg_files)
    compImg_fileQ = Queue(compImg_num)
    for i in range(compImg_num):
        compImg_fileQ.put((compImg_files[i], compImg_names[i]))

    processes = []
    for i in range(PROCESS_NUM):
        p = single_compare_process("compare-" + str(i), origImg, csv_file, compImg_fileQ, output_path, suffix)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    compImg_fileQ.close()