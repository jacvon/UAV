import cv2  # opencv-python==3.4.2.16, opencv-contrib-python==3.4.2.16
import numpy as np
from multiprocessing import freeze_support
from multiprocessing import Process, Queue
import os
import time
import csv

from numba import jit
from scipy import interpolate
import compare.image_similarity_model as ism
import compare.image_compare as icp
from offlineTask.models import SingleImageCompareInfo, OfflineTask


class single_compare_process(Process):

    def __init__(self, name, origImg, csv_file, compImg_fileQ, output_path, suffix=".jpg"):
        Process.__init__(self)
        self.name = name
        self.origImg = origImg
        self.csv_file = csv_file
        self.compImg_fileQ = compImg_fileQ
        self.output_path = output_path
        self.suffix = suffix
        self.__is_predict = True

    def run(self):
        print("Starting " + self.name + " Process")
        try:
            with open(self.csv_file, mode='r') as file_handle:
                csv_rows = csv.reader(file_handle)
                arr_gps = np.array([row for index, row in enumerate(csv_rows) if index > 0], dtype=np.float64)

            # Spline内插值且外推拟合（s=0时拟合曲线过各样本点，k<5为样条插值阶次）
            x_indexs = np.argsort(arr_gps[:, 2])
            y_indexs = np.argsort(arr_gps[:, 3])
            x_predict_func = interpolate.UnivariateSpline(arr_gps[x_indexs, 2], arr_gps[x_indexs, 0], k=3, s=0)
            y_predict_func = interpolate.UnivariateSpline(arr_gps[y_indexs, 3], arr_gps[y_indexs, 1], k=3, s=0)

            _, mask = cv2.threshold(cv2.cvtColor(self.origImg, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
            _, orig_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            print("不能通过CSV文件加载GPS信息进行位置插值:", e)
            self.__is_predict = False
            x_predict_func = None
            y_predict_func = None
            orig_contours = None

        similarity = ism.ImageSimilarity()
        similarity.batch_size = 32

        while (not self.compImg_fileQ.empty()):
            compImg_file, compImg_name = self.compImg_fileQ.get()
            compImg = icp.get_square_img(cv2.imread(compImg_file))
            predict_img = None
            predict_transArr = None

            compImg_gps = icp.get_gps(compImg_file)
            if (compImg_gps is not None) and (self.__is_predict == True):
                predict_x = int(x_predict_func(np.array([compImg_gps[0]])))
                predict_y = int(y_predict_func(np.array([compImg_gps[1]])))
                for cnt in orig_contours:
                    if cv2.pointPolygonTest(cnt, (predict_x, predict_y), False) >= 0:
                        h, w, _ = compImg.shape
                        predict_img = np.zeros_like(self.origImg)
                        cv2.rectangle(predict_img, (predict_x - int(w / 2), predict_y - int(h / 2)),
                                      (predict_x + int(w / 2), predict_y + int(h / 2)), (255, 255, 255), -1)
                        predict_img = cv2.bitwise_and(self.origImg, predict_img)

                        _, mask = cv2.threshold(cv2.cvtColor(predict_img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
                        left, right, top, bottom = icp.calc_bound(mask)
                        predict_img = predict_img[top:bottom + 1, left:right + 1]

                        h, w, _ = predict_img.shape
                        src_rect = np.float32([[left, top], [left, bottom], [right, bottom], [right, top]]).reshape(-1, 1, 2)
                        dst_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                        predict_transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)
                        break
                else:
                    print("Warning:", compImg_name, "GPS位置可能位于比对图像区域外，不进行位置预测。")
            else:
                print("Warning:", compImg_name, "不能通过GPS位置插值来进行位置预测。")

            if predict_img is None:
                predict_img = self.origImg
            img_list, contours = icp.getOverlayImgRegions(icp.getShrinkImg(self.origImg, scale=1.0), icp.getShrinkImg(compImg, scale=1.0),
                                                          compImg_name, icp.getShrinkImg(predict_img, scale=1.0), predict_transArr)
            ImgPosition, origImgRegion, compImgRegion = tuple(img_list)

            cv2.drawContours(ImgPosition, contours, -1, (0, 0, 255), 10)
            (x, y, w, h) = cv2.boundingRect(icp.findMaxAreaContour(contours))
            cv2.putText(ImgPosition, "Searched from " + compImg_name, (x + int(w / 4), y + int(h / 2)),
                        cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 3)
            temp_name = os.path.splitext(compImg_name)[0]
            cv2.imwrite(self.output_path + temp_name + "-Position" + self.suffix, ImgPosition)

            selected_boxs = icp.getSelectedBoxs(compImgRegion)
            # possible_boxs, other_box = ImageCompare_Hist(origImgRegion, compImgRegion, selected_boxs)
            possible_boxs, other_box = icp.ImageCompare_Deep(origImgRegion, compImgRegion, selected_boxs, similarity)
            for (x, y, w, h) in possible_boxs:
                cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
                cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
            '''
            for (x, y, w, h) in other_box:
                cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
            '''
            cv2.putText(origImgRegion, "Oringinal from " + compImg_name, (1, origImgRegion.shape[0] - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
            cv2.putText(compImgRegion, "Compared from " + compImg_name, (1, compImgRegion.shape[0] - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
            cv2.imwrite(self.output_path + temp_name + "-OrigRegion" + self.suffix, origImgRegion)
            cv2.imwrite(self.output_path + temp_name + "-CompRegion" + self.suffix, compImgRegion)

            print(self.name + " process image: " + compImg_name)
        print("Exitting " + self.name + " Process")

"""
if __name__ == '__main__':
    start_time = time.time()

    print('CPU核心数量:', cv2.getNumberOfCPUs())
    freeze_support()
    PROCESS_NUM = 2
    input_path = "./imgs/input_images/"
    output_path = "./imgs/output_images/"
    suffix = ".JPG"

    origImg = cv2.imread("./imgs/merged_img.JPG")
    csv_file = "./imgs/gps_points.csv"
    compImg_files, compImg_names = icp.getImgList(input_path, suffix, reverse=False)
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
    total_time = time.time() - start_time
    print('total cost time:', total_time)
"""

class predict_process(Process):
    def __init__(self, name, origImg, csv_file, compImg_fileQ, predict_regionQ):
        Process.__init__(self)
        self.name = name
        self.origImg = origImg
        self.csv_file = csv_file
        self.compImg_fileQ = compImg_fileQ
        self.predict_regionQ = predict_regionQ
        self.__is_predict = True

    def run(self):
        print("Starting " + self.name + " Process")
        try:
            with open(self.csv_file, mode='r') as file_handle:
                csv_rows = csv.reader(file_handle)
                arr_gps = np.array([row for index, row in enumerate(csv_rows) if index > 0], dtype=np.float64)

            # Spline内插值且外推拟合（s=0时拟合曲线过各样本点，k<5为样条插值阶次）
            x_indexs = np.argsort(arr_gps[:, 2])
            y_indexs = np.argsort(arr_gps[:, 3])
            x_predict_func = interpolate.UnivariateSpline(arr_gps[x_indexs, 2], arr_gps[x_indexs, 0], k=3, s=0)
            y_predict_func = interpolate.UnivariateSpline(arr_gps[y_indexs, 3], arr_gps[y_indexs, 1], k=3, s=0)

            _, mask = cv2.threshold(cv2.cvtColor(self.origImg, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
            _, orig_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            print("Exception:", e)
            print("Warning:不能通过CSV文件加载GPS信息进行位置插值.")
            self.__is_predict = False
            x_predict_func = None
            y_predict_func = None
            orig_contours = None


        while (not self.compImg_fileQ.empty()):
            compImg_file, compImg_name = self.compImg_fileQ.get()
            compImg = icp.get_square_img(cv2.imdecode(np.fromfile(compImg_file, dtype=np.uint8), 1))
            predict_img = None
            predict_transArr = None

            compImg_gps = icp.get_gps(compImg_file)
            if (compImg_gps is not None) and (self.__is_predict == True):
                predict_x = int(x_predict_func(np.array([compImg_gps[0]])))
                predict_y = int(y_predict_func(np.array([compImg_gps[1]])))
                for cnt in orig_contours:
                    if cv2.pointPolygonTest(cnt, (predict_x, predict_y), False) >= 0:
                        h, w, _ = compImg.shape
                        predict_img = np.zeros_like(self.origImg)
                        cv2.rectangle(predict_img, (predict_x - int(w / 2), predict_y - int(h / 2)),
                                      (predict_x + int(w / 2), predict_y + int(h / 2)), (255, 255, 255), -1)
                        predict_img = cv2.bitwise_and(self.origImg, predict_img)

                        _, mask = cv2.threshold(cv2.cvtColor(predict_img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
                        left, right, top, bottom = icp.calc_bound(mask)
                        predict_img = predict_img[top:bottom + 1, left:right + 1]

                        h, w, _ = predict_img.shape
                        src_rect = np.float32([[left, top], [left, bottom], [right, bottom], [right, top]]).reshape(-1, 1, 2)
                        dst_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                        predict_transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)
                        break
                else:
                    print("Warning:", compImg_name, "GPS位置可能位于比对图像区域外，不进行位置预测。")
            else:
                print("Warning:", compImg_name, "不能通过GPS位置插值来进行位置预测。")

            self.predict_regionQ.put((compImg, compImg_name, predict_img, predict_transArr))
            print("predict image: " + compImg_name)
        print("Exitting " + self.name + " Process")


class search_process(Process):
    def __init__(self, name, origImg, compImg_num, predict_regionQ, compImg_regionQ, search_regionQ, pos_regionQ):
        Process.__init__(self)
        self.name = name
        self.origImg = origImg
        self.compImg_num = compImg_num
        self.predict_regionQ = predict_regionQ
        self.compImg_regionQ = compImg_regionQ
        self.search_regionQ = search_regionQ
        self.pos_regionQ = pos_regionQ

    def run(self):
        print("Starting " + self.name + " Process")
        for i in range(self.compImg_num):
            compImg, compImg_name, predict_img, predict_transArr = self.predict_regionQ.get()
            if predict_img is None:
                predict_img = self.origImg
            img_list, contours = icp.getOverlayImgRegions(icp.getShrinkImg(self.origImg, scale=1.0), icp.getShrinkImg(compImg, scale=1.0),
                                                          compImg_name, icp.getShrinkImg(predict_img, scale=1.0), predict_transArr)
            if img_list is None or contours is None:
                self.compImg_regionQ.put((None, compImg_name))
                self.search_regionQ.put((None, None, compImg_name))
                self.pos_regionQ.put((None, None, compImg_name))
                continue
            ImgPosition, origImgRegion, compImgRegion = tuple(img_list)
            self.compImg_regionQ.put((compImgRegion, compImg_name))
            self.search_regionQ.put((origImgRegion, compImgRegion, compImg_name))
            self.pos_regionQ.put((ImgPosition, contours, compImg_name))
            print("search image: " + compImg_name)
        print("Exitting " + self.name + " Process")


class getboxs_process(Process):
    def __init__(self, name, compImg_num, compImg_regionQ, box_listQ):
        Process.__init__(self)
        self.name = name
        self.compImg_num = compImg_num
        self.compImg_regionQ = compImg_regionQ
        self.box_listQ = box_listQ

    def run(self):
        print("Starting " + self.name + " Process")
        for i in range(self.compImg_num):
            compImgRegion, compImg_name = self.compImg_regionQ.get()
            if compImgRegion is not None:
                selected_boxs = icp.getSelectedBoxs(compImgRegion)
                self.box_listQ.put(selected_boxs)
            else:
                self.box_listQ.put(None)
            print("get boxs from image: " + compImg_name)
        print("Exitting " + self.name + " Process")


class compare_process(Process):
    def __init__(self, name, compImg_num, search_regionQ, box_listQ, compare_regionQ):
        Process.__init__(self)
        self.name = name
        self.compImg_num = compImg_num
        self.search_regionQ = search_regionQ
        self.box_listQ = box_listQ
        self.compare_regionQ = compare_regionQ

    def run(self):
        print("Starting " + self.name + " Process")
        similarity = ism.ImageSimilarity()
        similarity.batch_size = 32
        for i in range(self.compImg_num):
            origImgRegion, compImgRegion, compImg_name = self.search_regionQ.get()
            selected_boxs = self.box_listQ.get()
            # possible_boxs, other_box = ImageCompare_Hist(origImgRegion, compImgRegion, selected_boxs)
            if (origImgRegion is not None) \
                    and (compImgRegion is not None) \
                    and (selected_boxs is not None):
                possible_boxs, other_box = icp.ImageCompare_Deep(origImgRegion, compImgRegion, selected_boxs, similarity)
                for (x, y, w, h) in possible_boxs:
                    cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
                    cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
                '''
                for (x, y, w, h) in other_box:
                    cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
                    cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
                '''
                self.compare_regionQ.put((origImgRegion, compImgRegion))
            else:
                self.compare_regionQ.put((None, None))
            print("compare image: " + compImg_name)
        print("Exitting " + self.name + " Process")


def saveSingleCompare(userOverdate, userTitleId, imageComOriginPanoPath, imageComOriginPartPath,
                      imageComOriginResultPath, progress, ImgPosition):
    singleImageCompare = SingleImageCompareInfo()

    singleImageCompare.overDate =userOverdate
    singleImageCompare.titleId = userTitleId
    singleImageCompare.is_compare = True
    if ImgPosition is None:
        singleImageCompare.is_show = 2
        singleImageCompare.imageComOriginPanoPath = None
        singleImageCompare.imageComOriginPartPath = None
        singleImageCompare.imageComOriginResultPath = None
    else:
        singleImageCompare.is_show = 1
        singleImageCompare.imageComOriginPanoPath = imageComOriginPanoPath
        singleImageCompare.imageComOriginPartPath = imageComOriginPartPath
        singleImageCompare.imageComOriginResultPath = imageComOriginResultPath
    singleImageCompare.progress = progress

    singleImageCompare.save()

    users = OfflineTask.objects.all()
    if int(progress) == 1:
        for user in users:
            if user.overDate == userOverdate:
                user.comparison_status = 'd'
                user.save()


class output_process(Process):
    def __init__(self, userOverdate, userTitleId, name, compImg_num, pos_regionQ, compare_regionQ, output_path, suffix=".jpg"):
        Process.__init__(self)
        self.userOverdate = userOverdate
        self.userTitleId = userTitleId
        self.name = name
        self.compImg_num = compImg_num
        self.pos_regionQ = pos_regionQ
        self.compare_regionQ = compare_regionQ
        self.output_path = output_path
        self.suffix = suffix

    def run(self):
        print("Starting " + self.name + " Process")
        imageComOriginPartPath = ''
        imageComOriginPanoPath = ''
        imageComOriginResultPath = ''
        for i in range(self.compImg_num):
            ImgPosition, contours, compImg_name = self.pos_regionQ.get()
            if (ImgPosition is not None) \
                    and (contours is not None):
                temp_name = os.path.splitext(compImg_name)[0]

                cv2.drawContours(ImgPosition, contours, -1, (0, 0, 255), 10)
                (x, y, w, h) = cv2.boundingRect(icp.findMaxAreaContour(contours))
                cv2.putText(ImgPosition, "Searched from " + compImg_name, (x + int(w / 4), y + int(h / 2)),
                        cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 3)
                #cv2.imwrite(self.output_path + temp_name + "-Position" + self.suffix, ImgPosition)
                imageComOriginPanoPath = self.output_path + temp_name + "-Position" + self.suffix
                cv2.imencode('.jpg', ImgPosition)[1].tofile(imageComOriginPanoPath)
                origImgRegion, compImgRegion = self.compare_regionQ.get()

                cv2.putText(origImgRegion, "Oringinal from " + compImg_name, (1, origImgRegion.shape[0] - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                cv2.putText(compImgRegion, "Compared from " + compImg_name, (1, compImgRegion.shape[0] - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                #cv2.imwrite(self.output_path + temp_name + "-OrigRegion" + self.suffix, origImgRegion)
                #cv2.imwrite(self.output_path + temp_name + "-CompRegion" + self.suffix, compImgRegion)
                imageComOriginPartPath = self.output_path + temp_name + "-OrigRegion" + self.suffix
                imageComOriginResultPath = self.output_path + temp_name + "-CompRegion" + self.suffix
                cv2.imencode('.jpg', origImgRegion)[1].tofile(imageComOriginPartPath)
                cv2.imencode('.jpg', compImgRegion)[1].tofile(imageComOriginResultPath)
            else:
                _, _ = self.compare_regionQ.get()
            saveSingleCompare(self.userOverdate, self.userTitleId, imageComOriginPanoPath,
                              imageComOriginPartPath, imageComOriginResultPath,
                              (i+1)/float(self.compImg_num),ImgPosition)
            print("output image: " + compImg_name)
        print("Exitting " + self.name + " Process")

def find_rows_cols(name_list):
    rows, cols = 0, 0
    for name in name_list:
        if "-" in name:
            (num_str, _) = os.path.splitext(name)
            num = num_str.split("-")
            r, c = int(num[0]) + 1, int(num[1]) + 1
            if rows < r:
                rows = r
            if cols < c:
                cols = c
    return rows, cols

def load_sliced_image(load_path, suffix=".jpg"):
    print(load_path)
    assert os.path.isdir(load_path), "can't find sliced image file path."
    all_file_names = os.listdir(load_path)
    name_list = [f for f in all_file_names if f.endswith(suffix)]
    ##name_list = sorted(name_list, reverse=False)

    ##(num_str, _) = os.path.splitext(name_list[-2])  # 倒数第二个切片文件名字能代表切片组的行列数量
    ##num = num_str.split("-")
    ##rows, cols = int(num[0]) + 1, int(num[1]) + 1
    rows, cols = find_rows_cols(name_list)
    #slice = cv2.imread(load_path + "0-0.jpg")
    slice = cv2.imdecode(np.fromfile(load_path +"0-0.jpg", dtype=np.uint8), 1)
    h, w = slice.shape[0:2]
    image = np.zeros((h * rows, w * cols, 3), np.uint8)
    for i in range(rows):
        for j in range(cols):
            slice_name = str(i) + "-" + str(j) + ".jpg"
            #slice = cv2.imread(load_path + slice_name)
            slice = cv2.imdecode(np.fromfile(load_path + slice_name, dtype=np.uint8), 1)
            image[i * h:(i + 1) * h, j * w:(j + 1) * w] = slice

    # 求图像右侧和下侧非全黑边边界
    @jit(nopython=True)
    def calc_bound(gray):
        bottom, right = gray.shape[0:2]
        for col in range(gray.shape[1] - 1, 0, -1):
            if gray[:, col].any():
                right = col
                break
        for row in range(gray.shape[0] - 1, 0, -1):
            if gray[row, :].any():
                bottom = row
                break
        return right, bottom
    right, bottom = calc_bound(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return image[0:bottom + 1, 0:right + 1]

def compare_handle(originPath, savePath, historyPath, historyGpsPath, userOverdate, userTitleId):
    start_time = time.time()
    print('CPU核心数量:', cv2.getNumberOfCPUs())
    freeze_support()
    input_path = originPath
    output_path = savePath
    suffix = ".JPG"

    #origImg = cv2.imread(historyPath)
    #origImg = cv2.imdecode(np.fromfile(historyPath, dtype=np.uint8), 1)
    path, file = os.path.split(historyPath)
    origImg = load_sliced_image(path+'/', suffix=".jpg")
    csv_file = historyGpsPath

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    compImg_files, compImg_names = icp.getImgList(input_path, suffix, reverse=False)
    compImg_num = len(compImg_files)
    compImg_fileQ = Queue(compImg_num)
    for i in range(compImg_num):
        compImg_fileQ.put((compImg_files[i], compImg_names[i]))

    predict_regionQ = Queue(4)
    compImg_regionQ = Queue(4)
    box_listQ = Queue(4)
    search_regionQ = Queue(4)
    pos_regionQ = Queue(4)
    compare_regionQ = Queue(4)

    processes = []
    process_pp = predict_process("predict_process", origImg, csv_file, compImg_fileQ, predict_regionQ)
    process_pp.start()
    processes.append(process_pp)

    process_sp = search_process("search_process", origImg, compImg_num, predict_regionQ, compImg_regionQ, search_regionQ, pos_regionQ)
    process_sp.start()
    processes.append(process_sp)

    process_gp = getboxs_process("getboxs_process", compImg_num, compImg_regionQ, box_listQ)
    process_gp.start()
    processes.append(process_gp)

    process_cp = compare_process("compare_process", compImg_num, search_regionQ, box_listQ, compare_regionQ)
    process_cp.start()
    processes.append(process_cp)

    process_op = output_process(userOverdate, userTitleId, "outpu_process", compImg_num, pos_regionQ, compare_regionQ, output_path, suffix)
    process_op.start()
    processes.append(process_op)

    #for p in processes:
        #p.join()

    #compImg_fileQ.close()
    #predict_regionQ.close()
    #compImg_regionQ.close()
    #box_listQ.close()
    #search_regionQ.close()
    #pos_regionQ.close()
    #compare_regionQ.close()
    total_time = time.time() - start_time
    print('total cost time:', total_time)