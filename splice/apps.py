import csv
import splice.image_mosiac as ims
from multiprocessing import Process, Event, Queue
import cv2
import numpy as np

from offlineTask.models import SingleImageSpliceInfo


def saveSingleSplice(progress, userOverDate, userTitleId, imageSplicePath, gpsCsvPath):
    singleImageSplice = SingleImageSpliceInfo()

    singleImageSplice.titleId=userTitleId
    singleImageSplice.progress = progress
    singleImageSplice.overDate = userOverDate
    singleImageSplice.is_show = False
    singleImageSplice.is_splice = True
    singleImageSplice.imageSplicePath = imageSplicePath
    singleImageSplice.imagePreprocessPath = imageSplicePath.replace('splice', 'preprocess')
    singleImageSplice.gpsCsvPath = gpsCsvPath
    singleImageSplice.save()

class transform_process(Process):
    def __init__(self, name, numQ, enhancedQ, transformedQ, num_evt):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.enhancedQ = enhancedQ
        self.transformedQ = transformedQ
        self.num_evt = num_evt

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        self.__transform(img_num)
        print("Exitting " + self.name + " Process")

    def __transform(self, img_num):
        priorImg = None  # 用于保存前一张图像
        priorName = None  # 用于保存前一张图像文件名
        count = 0
        PerArrs = []
        Shapes = []
        while count < img_num:
            enhanced_img, img_name, gps_info = self.enhancedQ.get()
            img = ims.get_square_img(enhanced_img, Flag = True)
            if count > 0:
                per_arr = ims.getTransformMatrix(priorImg, priorName, img, img_name)  # 求取变换矩阵
                PerArrs.append(per_arr)
                Shapes.append(img.shape)
                min_left_bound, min_top_bound, max_right_bound, max_bottom_bound = ims.getMaxBoundary(PerArrs, Shapes)  # 获取拼接图像的最大边界
                new_width, new_height = (max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

                # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
                src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                                       [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
                dst_rect = np.float32([[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1], [new_width - 1, 0]]).reshape(-1, 1,
                                                                                                                                  2)
                transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)

                perArr = ims.PerArrs_Mutiply(PerArrs, count)  # 透射变换矩阵的叠加连乘
                perArr = np.dot(transArr, perArr)  # 计算平移时的透射变换矩阵

                h, w, _ = img.shape
                center_point = np.float32([[w / 2, h / 2]]).reshape(-1, 1, 2)
                center_point = cv2.perspectiveTransform(center_point, perArr)
                # 可选cv2.INTER_LINEAR，但可能会出现黑色边缘锯齿
                # 使用cv2.WARP_INVERSE_MAP，则要求逆矩阵np.linalg.inv(perArr)
                warpImg = cv2.warpPerspective(img, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)
                self.transformedQ.put((warpImg, img_name, transArr, [new_width, new_height], center_point.reshape(-1, 2), gps_info))
                print("transformed image : " + img_name)
            else:
                Shapes.append(img.shape)
                h, w, _ = img.shape
                center_point = np.float32([[w / 2, h / 2]]).reshape(-1, 2)
                self.transformedQ.put((img, None, None, [None, None], center_point, gps_info))

            priorImg = np.copy(img)
            priorName = img_name
            count += 1
        return None


class seam_process(Process):
    def __init__(self, name, userOverdate, userTitleId, numQ, transformedQ, num_evt, save_path, suffix=".jpg", is_each_save=False):
        Process.__init__(self)
        self.name = name
        self.userOverdate = userOverdate
        self.userTitleId = userTitleId
        self.numQ = numQ
        self.transformedQ = transformedQ
        self.num_evt = num_evt
        self.save_path = save_path
        self.suffix = suffix
        self.is_each_save = is_each_save
        self.__gps_points = np.zeros(2, dtype=np.float32).reshape(-1, 2)
        self.__gps_infos = np.zeros(3, dtype=np.float64).reshape(-1, 3)

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        merged_img = self.__getBeamImage(img_num)
        # TODO: 纠正倾斜
        '''
        _, mask = cv2.threshold(cv2.cvtColor(merged_img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = np.array(contours[0], dtype=np.int32).reshape(-1,2)
        left_x = np.min(contours[:, 0])
        right_x = np.max(contours[:, 0])
        top_y = np.min(contours[:, 1])
        bottom_y = np.max(contours[:, 1])
        h, w, _ = merged_img.shape
        src_rect = np.float32([[left_x, top_y], [left_x, bottom_y], [right_x, bottom_y],
                               [right_x, top_y]]).reshape(-1, 1, 2)
        dst_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)
        merged_img = cv2.warpPerspective(merged_img, transArr, (w, h), flags=cv2.INTER_NEAREST)
        '''
        #cv2.imwrite(self.save_path + "merged_img" + self.suffix, cv2.medianBlur(merged_img, 3)) # 保存拼接图像
        cv2.imencode('.jpg', cv2.medianBlur(merged_img, 3))[1].tofile(self.save_path + "merged_img" + self.suffix)
        with open(self.save_path + "gps_points.csv", mode='w', newline='') as file_handle:
            file_csv = csv.writer(file_handle)
            header = ['point_x', 'point_y', 'longitude', 'latitude', 'altitude']
            file_csv.writerow(header)
            for i in range(len(self.__gps_points)):
                if self.__gps_infos[i] is not None:
                    item = [self.__gps_points[i][0], self.__gps_points[i][1], '{0:.8f}'.format(self.__gps_infos[i][0]),
                            '{0:.10f}'.format(self.__gps_infos[i][1]), self.__gps_infos[i][2]]
                    file_csv.writerow(item)
        saveSingleSplice(1, self.userOverdate, self.userTitleId, self.save_path + "merged_img" + self.suffix, self.save_path + "gps_points.csv")
        print("Exitting " + self.name + " Process")

    def __getBeamImage(self, img_num):
        mergeImg = None  # 用于保存当前拼接的图像
        priorArrs = [np.eye(3, dtype=np.float32)]
        count = 0
        while count < img_num:
            warpImg, img_name, transArr, new_shape, center_point, gps_info = self.transformedQ.get()
            if count > 0:
                # 当前已拼接图的平移
                perArr = ims.PerArrs_Mutiply(np.linalg.inv(priorArrs), count)  # 利用求逆矩阵恢复到第一张基准图的原始坐标
                perArr = np.dot(transArr, perArr)  # 计算平移时的新透射变换矩阵
                mergeImg = cv2.warpPerspective(mergeImg, perArr, (new_shape[0], new_shape[1]), flags=cv2.INTER_NEAREST)
                priorArrs.append(perArr)
                self.__gps_points = cv2.perspectiveTransform(self.__gps_points.reshape(-1, 1, 2), perArr).reshape(-1, 2)
                self.__gps_points = np.append(self.__gps_points, center_point, axis=0)
                self.__gps_infos = np.append(self.__gps_infos, gps_info, axis=0)

                mergeImg = ims.getOverlayImg_Seam(mergeImg, warpImg)  # 最佳缝合线拼接

                if self.is_each_save:
                    #cv2.imwrite(self.save_path + "merging_img" + str(count) + self.suffix, cv2.medianBlur(mergeImg, 3))  # 保存拼接后的图像
                    cv2.imencode('.jpg', cv2.medianBlur(mergeImg, 3))[1].tofile(
                        self.save_path + "merging_img" + str(count) + self.suffix)
                print("merged image : " + img_name)
            else:
                mergeImg = np.copy(warpImg)
                self.__gps_points = center_point
                self.__gps_infos = gps_info
            count += 1
            if count<img_num-1 :
                saveSingleSplice(count / float(img_num), self.userOverdate, self.userTitleId,
                                self.save_path + "merging_img" + str(count) + self.suffix, None)
        return mergeImg