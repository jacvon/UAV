import splice.image_mosiac as ims
from multiprocessing import freeze_support, cpu_count
from multiprocessing import Process, Event, Queue
import os
import cv2
import numpy as np
import time


class seam_process(Process):
    def __init__(self, name, numQ, transformedQ, num_evt, save_path, suffix, is_each_save):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.transformedQ = transformedQ
        self.num_evt = num_evt
        self.save_path = save_path
        self.suffix = suffix
        self.is_each_save = is_each_save

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        merged_img = self.getBeamImage(self.transformedQ, img_num, self.save_path, self.suffix, self.is_each_save)
        cv2.imwrite(self.save_path + "merged_img" + self.suffix, merged_img)  # 保存拼接图像
        print("Exitting " + self.name + " Process")

    def getBeamImage(self, imgQ, img_num, save_path="./", suffix=".jpg", is_each_save=False):
        mergeImg = None  # 用于保存当前拼接的图像
        priorArrs = [np.eye(3, dtype=np.float32)]
        count = 0
        while count < img_num:
            recv_data = imgQ.get()
            if count > 0:
                # 当前已拼接图的平移
                perArr = ims.PerArrs_Mutiply(np.linalg.inv(priorArrs), count)  # 利用求逆矩阵恢复到第一张基准图的原始坐标
                perArr = np.dot(recv_data[2], perArr)  # 计算平移时的新透射变换矩阵
                mergeImg = cv2.warpPerspective(mergeImg, perArr, (recv_data[3], recv_data[4]), flags=cv2.INTER_NEAREST)
                priorArrs.append(perArr)

                ##################################################################################
                # 通过调用getOverlayImg、getOverlayImg_Distance或getgetOverlayImg_Seam函数实现连续拼接
                # mergeImg = ims.getOverlayImg(mergeImg, 0.5, recv_data[0], 0.5)       # 重叠区各取50%，过渡不自然
                # mergeImg = ims.getOverlayImg_Distance(mergeImg, recv_data[0])      # 按距离设置权重，过渡相对自然
                mergeImg = ims.getOverlayImg_Seam(mergeImg, recv_data[0])  # 最佳缝合线拼接
                ##################################################################################

                if is_each_save:
                    cv2.imwrite(save_path + "merging_img" + str(count) + suffix, mergeImg)  # 保存拼接后的图像
                print("merged image : " + recv_data[1])
            else:
                mergeImg = np.copy(recv_data[0])
            count += 1
        return mergeImg


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
        self.transform(self.enhancedQ, self.transformedQ, img_num)
        print("Exitting " + self.name + " Process")

    def transform(self, imgQ, returnQ, img_num):
        priorImg = None  # 用于保存前一张图像
        priorName = None  # 用于保存前一张图像文件名
        count = 0
        PerArrs = []
        Shapes = []
        while count < img_num:
            recv_data = imgQ.get()
            img = ims.get_square_img(recv_data[0])
            if count > 0:
                per_arr = ims.getTransformMatrix(priorImg, priorName, img, recv_data[1])  # 求取变换矩阵
                PerArrs.append(per_arr)
                Shapes.append(img.shape)
                min_left_bound, min_top_bound, max_right_bound, max_bottom_bound = ims.getMaxBoundary(PerArrs, Shapes)  # 获取拼接图像的最大边界
                new_width, new_height = (max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

                # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
                src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                                       [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
                dst_rect = np.float32([[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1], [new_width - 1, 0]]).reshape(-1, 1, 2)
                transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)

                perArr = ims.PerArrs_Mutiply(PerArrs, count)  # 透射变换矩阵的叠加连乘
                perArr = np.dot(transArr, perArr)  # 计算平移时的透射变换矩阵
                # 可选cv2.INTER_LINEAR，但可能会出现黑色边缘锯齿
                # 使用cv2.WARP_INVERSE_MAP，则要求逆矩阵np.linalg.inv(perArr)
                warpImg = cv2.warpPerspective(img, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)
                returnQ.put([warpImg, recv_data[1], transArr, new_width, new_height])
                print("transformed image : " + recv_data[1])
            else:
                Shapes.append(img.shape)
                returnQ.put([img, None, None, None, None])

            priorImg = np.copy(img)
            priorName = recv_data[1]
            count += 1
        return None