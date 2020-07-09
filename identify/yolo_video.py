import os
import sys
import argparse
from multiprocessing import freeze_support
from multiprocessing import Process, Event, Queue

from offlineTask.models import SingleImageIdentifyInfo, OfflineTask
from yolo import YOLO, detect_video
from PIL import Image
import time
import cv2
import splice.image_stitch as ist
import numpy as np

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")

def saveIdentifyImage(progress, userOverdate, userTitleId, savePath):
    singleImageIdentifyInfo = SingleImageIdentifyInfo()

    singleImageIdentifyInfo.titleId = userTitleId
    singleImageIdentifyInfo.is_show = False
    singleImageIdentifyInfo.progress = progress
    singleImageIdentifyInfo.is_identify = False
    singleImageIdentifyInfo.imageIdentifyPath = savePath
    singleImageIdentifyInfo.overDate = userOverdate
    singleImageIdentifyInfo.save()

    users = OfflineTask.objects.all()
    if int(progress) == 1:
        for user in users:
            if user.overDate == userOverdate:
                user.identify_status = 'd'
                user.save()

class identify_yolo(Process):
    def __init__(self, name, userOverdate, userTitleId, numQ, loadedQ, num_evt, savePath, suffix=".jpg"):
        Process.__init__(self)
        self.name = name
        self.userOverdate = userOverdate
        self.userTitleId = userTitleId
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.num_evt = num_evt
        self.savePath = savePath
        self.suffix = suffix

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        self._identify(img_num)
        print("Exitting " + self.name + " Process")

    def _identify(self, img_num):
        count = 0
        yolo = YOLO()
        while count < img_num:
            img, img_name = self.loadedQ.get()
            r_image = yolo.detect_image(img)
            rawimg = np.array(r_image)
            cv2.imencode('.jpg', rawimg)[1].tofile(self.savePath + img_name)
            saveIdentifyImage((count+1)/float(img_num), self.userOverdate, self.userTitleId, self.savePath + img_name)
            count += 1
        print("Exitting " + self.name + " Process")

class identify_load(Process):
    def __init__(self, name, numQ, loadedQ, num_evt, load_path, suffix=".jpg"):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.num_evt = num_evt
        self.loadedQ = loadedQ
        self.load_path = load_path
        self.suffix = suffix

    def run(self):
        img_paths, img_names = ist.getImgList(self.load_path, self.suffix, reverse=False)
        next_stage_num = 2
        for i in range(next_stage_num):
            self.numQ.put(len(img_paths))
        self.num_evt.set()
        for index, img_path in enumerate(img_paths):
            #loaded_img = cv2.imread(img_path)
            #cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            image = Image.open(img_path)
            print(type(image),img_path)
            img_name = os.path.basename(img_path)
            #gps_info = ist.get_gps(img_path)
            self.loadedQ.put((image, img_name))
            print("loaded image: " + img_names[index])
        print("Exitting " + self.name + " Process")

def identify_handle(originPath, savePath, userOverdate, userTitleId):
    start_time = time.time()
    print('CPU核心数量:', cv2.getNumberOfCPUs())
    freeze_support()
    numQ = Queue(2)
    loadedQ = Queue(4)
    suffix = ".JPG"
    num_evt = Event()

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    processes = []
    process_lo = identify_load("identify_load", numQ, loadedQ, num_evt, originPath, suffix)
    process_lo.start()
    processes.append(process_lo)
    process_id = identify_yolo("identify_yolo", userOverdate, userTitleId, numQ, loadedQ, num_evt, savePath, suffix)
    process_id.start()
    processes.append(process_id)

    print("Exitting Main Process")
    total_time = time.time() - start_time
    print('total cost time:', total_time)