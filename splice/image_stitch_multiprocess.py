import splice.image_stitch as ist
from multiprocessing import freeze_support
from multiprocessing import Process, Event, Queue
import os
import cv2  # opencv-python==3.4.2.16, opencv-contrib-python==3.4.2.16
import numpy as np
import csv
import time

from offlineTask.models import SingleImageSpliceInfo, OfflineTask


def save_sliced_image(img, slice_size, save_path):
    H, W = img.shape[0:2]
    h, w = slice_size

    # 保存缩略图
    if H / W >= h / w:
        tx, ty = h * W // H, h
    else:
        tx, ty = w, w * H // W
    thumbnail = cv2.resize(img, (tx*5, ty*5), interpolation=cv2.INTER_AREA)
    #cv2.imwrite(save_path + "thumbnail.jpg", thumbnail, [cv2.IMWRITE_JPEG_QUALITY, 100])
    cv2.imencode('.jpg', thumbnail)[1].tofile(save_path + "thumbnail.jpg")
    # 保存切片图
    rows = H // h if H % h == 0 else H // h + 1
    cols = W // w if W % w == 0 else W // w + 1

    for i in range(rows):
        for j in range(cols):
            image_slice = np.zeros((h, w, 3), np.uint8)
            if i == rows - 1:
                if j == cols - 1:
                    image_slice[0:H - i * h, 0:W - j * w] = img[i * h:H, j * w:W]
                else:
                    image_slice[0:H - i * h, :] = img[i * h:H, j * w:(j + 1) * w]
            else:
                if j == cols - 1:
                    image_slice[:, 0:W - j * w] = img[i * h:(i + 1) * h, j * w:W]
                else:
                    image_slice = img[i * h:(i + 1) * h, j * w:(j + 1) * w]
            #cv2.imwrite(save_path + str(i) + "-" + str(j) + ".jpg", image_slice, [cv2.IMWRITE_JPEG_QUALITY, 100])
            cv2.imencode('.jpg', image_slice)[1].tofile(save_path + str(i) + "-" + str(j) + ".jpg")

def saveSingleSplice(progress, userOverDate, userTitleId, imageSplicePath, gpsCsvPath):
    singleImageSplice = SingleImageSpliceInfo()

    singleImageSplice.titleId=userTitleId
    singleImageSplice.progress = progress
    singleImageSplice.overDate = userOverDate
    singleImageSplice.is_show = False
    singleImageSplice.is_splice = True
    singleImageSplice.imageSplicePath = imageSplicePath
    singleImageSplice.gpsCsvPath = gpsCsvPath
    singleImageSplice.save()

    users = OfflineTask.objects.all()
    if int(progress) == 1:
        for user in users:
            if user.overDate == userOverDate:
                user.splice_status = 'd'
                user.save()

class load_process(Process):
    def __init__(self, name, numQ, loadedQ, num_evt, load_path, suffix=".jpg"):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.num_evt = num_evt
        self.load_path = load_path
        self.suffix = suffix

    def run(self):
        print("Starting " + self.name + " Process")
        img_paths, img_names = ist.getImgList(self.load_path, self.suffix, reverse=False)
        next_stage_num = 2
        for i in range(next_stage_num):
            self.numQ.put(len(img_paths))
        self.num_evt.set()
        for index, img_path in enumerate(img_paths):
            #loaded_img = cv2.imread(img_path)
            loaded_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
            img_name = os.path.basename(img_path)
            gps_info = ist.get_gps(img_path)
            self.loadedQ.put((loaded_img, img_name, gps_info))
            print("loaded image: " + img_names[index])
        print("Exitting " + self.name + " Process")

class transform_process(Process):
    def __init__(self, name, numQ, loadedQ, transformedQ, num_evt):
        Process.__init__(self)
        self.name = name
        self.numQ = numQ
        self.loadedQ = loadedQ
        self.transformedQ = transformedQ
        self.num_evt = num_evt

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        self._transform(img_num)
        print("Exitting " + self.name + " Process")

    def _transform(self, img_num):
        priorImg = None  # 用于保存前一张图像
        priorName = None  # 用于保存前一张图像文件名
        count = 0
        PerArrs = []
        Shapes = []
        while count < img_num:
            img, img_name, gps_info = self.loadedQ.get()
            img = ist.get_square_img(img, Flag=False)
            if count > 0:
                per_arr = ist.getTransformMatrix(priorImg, priorName, img, img_name)  # 求取变换矩阵
                PerArrs.append(per_arr)
                Shapes.append(img.shape)
                min_left_bound, min_top_bound, max_right_bound, max_bottom_bound = ist.getMaxBoundary(PerArrs, Shapes)  # 获取拼接图像的最大边界
                new_width, new_height = (max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

                # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
                src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                                       [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
                dst_rect = np.float32([[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1], [new_width - 1, 0]]).reshape(-1, 1, 2)
                transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)

                perArr = ist.PerArrs_Mutiply(PerArrs, count)  # 透射变换矩阵的叠加连乘
                perArr = np.dot(transArr, perArr)  # 计算平移时的透射变换矩阵

                h, w, _ = img.shape
                center_point = np.float32([[w / 2, h / 2]]).reshape(-1, 1, 2)
                center_point = cv2.perspectiveTransform(center_point, perArr)
                # 可选cv2.INTER_LINEAR，但可能会出现黑色边缘锯齿
                # 使用cv2.WARP_INVERSE_MAP，则要求逆矩阵np.linalg.inv(perArr)
                warpImg = cv2.warpPerspective(img, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)
                self.transformedQ.put((warpImg, img_name, transArr, [new_width, new_height], center_point.reshape(-1, 2), gps_info))
                print("transformed image: " + img_name)
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
    def __init__(self,userOverdate, userTitleId, name, numQ, transformedQ, num_evt, save_path, suffix=".jpg", is_each_save=False):
        Process.__init__(self)
        self.userOverdate = userOverdate
        self.userTitleId = userTitleId
        self.name = name
        self.numQ = numQ
        self.transformedQ = transformedQ
        self.num_evt = num_evt
        self.save_path = save_path
        self.suffix = suffix
        self.is_each_save = is_each_save
        self._gps_points = np.zeros(2, dtype=np.float32).reshape(-1, 2)
        self._gps_infos = np.zeros(3, dtype=np.float64).reshape(-1, 3)

    def run(self):
        print("Starting " + self.name + " Process")
        self.num_evt.wait()
        img_num = self.numQ.get()
        merged_img = self._getBeamImage(img_num)
        # TODO: 纠正倾斜 + 两两拼接
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
        transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)
        merged_img = cv2.warpPerspective(merged_img, transArr, (w, h), flags=cv2.INTER_NEAREST)
        '''
        #cv2.imwrite(self.save_path + "merged_img" + self.suffix, merged_img)  # 保存拼接图像
        #cv2.imencode('.jpg', merged_img)[1].tofile(self.save_path + "merged_img" + self.suffix)
        slice_size = (400, 640)
        save_sliced_image(merged_img, slice_size, self.save_path)
        with open(self.save_path + "gps_points.csv", mode='w', newline='') as file_handle:
            file_csv = csv.writer(file_handle)
            header = ['point_x', 'point_y', 'longitude', 'latitude', 'altitude']
            file_csv.writerow(header)
            for i in range(len(self._gps_points)):
                if self._gps_infos[i] is not None:
                    item = [self._gps_points[i][0], self._gps_points[i][1], '{0:.10f}'.format(self._gps_infos[i][0]),
                            '{0:.10f}'.format(self._gps_infos[i][1]), self._gps_infos[i][2]]
                    file_csv.writerow(item)
        saveSingleSplice(1, self.userOverdate, self.userTitleId, self.save_path + "thumbnail" + self.suffix,
                         self.save_path + "gps_points.csv")
        print("Exitting " + self.name + " Process")

    def _getBeamImage(self, img_num):
        mergeImg = None  # 用于保存当前拼接的图像
        priorArrs = [np.eye(3, dtype=np.float64)]
        count = 0
        former_direction = None
        while count < img_num:
            warpImg, img_name, transArr, new_shape, center_point, gps_info = self.transformedQ.get()
            if count > 0:
                # 当前已拼接图的平移
                perArr = ist.PerArrs_Mutiply(np.linalg.inv(priorArrs), count)  # 利用求逆矩阵恢复到第一张基准图的原始坐标
                perArr = np.dot(transArr, perArr)  # 计算平移时的新透射变换矩阵
                mergeImg = cv2.warpPerspective(mergeImg, perArr, (new_shape[0], new_shape[1]), flags=cv2.INTER_NEAREST)
                priorArrs.append(perArr)
                self._gps_points = cv2.perspectiveTransform(self._gps_points.reshape(-1, 1, 2), perArr).reshape(-1, 2)
                self._gps_points = np.append(self._gps_points, center_point, axis=0)
                self._gps_infos = np.append(self._gps_infos, gps_info, axis=0)

                last_flag = False  # 是否最后一张待拼接图
                if count == img_num - 1:
                    last_flag = True

                mergeImg, former_direction = ist.getOverlayImg_Seam(mergeImg, warpImg, former_direction, last_flag)  # 最佳缝合线拼接

                if self.is_each_save:
                    #cv2.imwrite(self.save_path + "merging_img" + str(count) + self.suffix, mergeImg)  # 保存拼接后的图像
                    cv2.imencode('.jpg', mergeImg)[1].tofile(
                        self.save_path + "merging_img" + str(count) + self.suffix)
                print("merged image: " + img_name)
            else:
                mergeImg = np.copy(warpImg)
                self._gps_points = center_point
                self._gps_infos = gps_info
            count += 1
            #if count < img_num - 1:
                #saveSingleSplice(count / float(img_num), self.userOverdate, self.userTitleId,
                                 #self.save_path + "merging_img" + str(count) + self.suffix, None)
        return mergeImg

def splice_handle(originPath, savePath, userOverdate, userTitleId,is_each_save=True):
    start_time = time.time()
    print('CPU核心数量:', cv2.getNumberOfCPUs())
    freeze_support()
    numQ = Queue(2)
    loadedQ = Queue(4)
    transformedQ = Queue(4)
    num_evt = Event()

    load_path = originPath
    merge_save_path = savePath
    suffix = ".JPG"
    is_each_save = False  # 保存每一步拼接过程的中间结果

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    processes = []
    process_lp = load_process("Image_Load", numQ, loadedQ, num_evt, load_path, suffix)
    process_lp.start()
    processes.append(process_lp)
    process_tp = transform_process("Image_Transform", numQ, loadedQ, transformedQ, num_evt)
    process_tp.start()
    processes.append(process_tp)
    process_sp = seam_process(userOverdate, userTitleId, "Image_Beam", numQ, transformedQ, num_evt, merge_save_path, suffix, is_each_save)
    process_sp.start()
    processes.append(process_sp)

    #for p in processes:
        #p.join()

    #numQ.close()
    #loadedQ.close()
    #transformedQ.close()
    print("Exitting Main Process")
    total_time = time.time() - start_time
    print('total cost time:', total_time)
