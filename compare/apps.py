import os
from multiprocessing import Process, Queue
import csv
import numpy as np
from scipy import interpolate
import cv2

from image_comparison import get_square_img, get_gps, getOverlayImgRegions, getShrinkImg, findMaxAreaContour, \
    ImageCompare_SSIM, cal_bound


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

        while (not self.compImg_fileQ.empty()):
            compImg_file, compImg_name = self.compImg_fileQ.get()
            compImg = get_square_img(cv2.imread(compImg_file))
            predict_img = None
            predict_transArr = None

            compImg_gps = get_gps(compImg_file)
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
                        left, right, top, bottom = cal_bound(mask)
                        predict_img = predict_img[top:bottom + 1, left:right + 1]

                        h, w, _ = predict_img.shape
                        src_rect = np.float32([[left, top], [left, bottom], [right, bottom], [right, top]]).reshape(-1, 1, 2)
                        dst_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                        predict_transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)
                        break
                else:
                    print("Warning:", compImg_name, "GPS位置可能位于比对图像区域外，不进行位置预测。")
            else:
                print("Warning:", compImg_name, "不能通过GPS位置插值来进行位置预测。")

            if predict_img is None:
                predict_img = self.origImg
            img_list, contours = getOverlayImgRegions(getShrinkImg(self.origImg, scale=1.0), getShrinkImg(compImg, scale=1.0),
                                                      compImg_name, getShrinkImg(predict_img, scale=1.0), predict_transArr)
            ImgPosition, origImgRegion, compImgRegion = tuple(img_list)

            cv2.drawContours(ImgPosition, contours, -1, (0, 0, 255), 10)
            (x, y, w, h) = cv2.boundingRect(findMaxAreaContour(contours))
            cv2.putText(ImgPosition, "Searched from " + compImg_name, (x + int(w / 4), y + int(h / 2)),
                        cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 3)
            temp_name = os.path.splitext(compImg_name)[0]
            cv2.imwrite(self.output_path + temp_name + "-Position" + self.suffix, ImgPosition)

            # possible_boxs, other_box = ImageCompare_SS(origImgRegion, compImgRegion)
            possible_boxs, other_box = ImageCompare_SSIM(origImgRegion, compImgRegion, isShowImg=False)
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