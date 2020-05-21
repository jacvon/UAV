import os
import shutil
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import convolve as fil_convolve
from scipy.signal import convolve as sig_convolve
from numba import jit


###剔除重叠冗余的图片###
def removeRedundantImgs(img_files, img_names):
    index = 1
    removed_indexs = []
    PerArrs, Shapes = getPerArrsAndShapes(img_files, img_names)

    while index < len(PerArrs):
        img0 = np.zeros((Shapes[index - 1][0], Shapes[index - 1][1]), np.uint8)
        area0 = float(img0.shape[0] * img0.shape[1])
        area01 = 0.0
        area02 = 0.0
        img1 = np.zeros((Shapes[index][0], Shapes[index][1]), np.uint8)
        area1 = float(img1.shape[0] * img1.shape[1])
        area12 = 0.0

        h, w = Shapes[index][0:2]
        pts1 = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst01 = cv2.perspectiveTransform(pts1, PerArrs[index - 1])
        img01_mask = cv2.fillPoly(img0.copy(), [np.int32(dst01)], 255)
        _, contours01, _ = cv2.findContours(img01_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        assert len(contours01) == 1, "the two images must have only one overlay area."

        area01 = cv2.contourArea(contours01[0])
        ratio01 = area01 / area0
        assert ratio01 > 0.2, "The overlap of the two images <{}, {}> is less than 20% <{:.1%}>." \
            .format(img_names[index - 1], img_names[index], ratio01)

        h, w = Shapes[index + 1][0:2]
        pts2 = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst12 = cv2.perspectiveTransform(pts2, PerArrs[index])
        img12_mask = cv2.fillPoly(img1.copy(), [np.int32(dst12)], 255)
        _, contours12, _ = cv2.findContours(img12_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        assert len(contours12) == 1, "the two images must have only one overlay area."

        area12 = cv2.contourArea(contours12[0])
        ratio12 = area12 / area1
        assert ratio12 > 0.2, "The overlap of the two images <{}, {}> is less than 20% <{:.1%}>." \
            .format(img_names[index], img_names[index + 1], ratio12)

        dst02 = cv2.perspectiveTransform(pts2, np.dot(PerArrs[index - 1], PerArrs[index]))
        img02_mask = cv2.fillPoly(img0.copy(), [np.int32(dst02)], 255)
        _, contours02, _ = cv2.findContours(img02_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        assert len(contours02) < 2, "the two images must have only one overlay area or no overlay area."

        if len(contours02) == 1:
            area02 = cv2.contourArea(contours02[0])
        ratio02 = area02 / area0

        if (ratio01 > 0.8 or ratio12 > 0.8) and ratio02 > 0.3:
            removed_indexs.append(index)
            index = index + 2
        else:
            index = index + 1

    ret_img_files = [img_files[i] for i in range(len(img_files)) if i not in removed_indexs]
    ret_img_names = [img_names[i] for i in range(len(img_files)) if i not in removed_indexs]
    return ret_img_files, ret_img_names


def getReducedImages(read_path, save_path, suffix=".jpg"):
    img_files, img_names = getImgList(read_path, suffix, reverse=False)
    assert len(img_files) >= 3, "need three images at least."

    while True:
        img_num = len(img_files)
        img_files, img_names = removeRedundantImgs(img_files, img_names)
        if img_num == len(img_files):
            break
    # 复制文件到保存路径
    for file in img_files:
        shutil.copy(file, save_path)
    return img_files, img_names


##################################  我 是 分 割 线  ##################################

def getImgList(path, suffix=".jpg", reverse=False, sort_by_time=False):
    assert os.path.isdir(path), "can't find image file path."
    all_file_names = os.listdir(path)

    name_list = [f for f in all_file_names if f.endswith(suffix)]
    if sort_by_time:
        # 按创建时间排序
        name_list = sorted(name_list, key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=reverse)
    else:
        # 按文件名排序
        name_list = sorted(name_list, reverse=reverse)

    file_list = [os.path.join(path, name) for name in name_list]
    return file_list, name_list


# 压缩处理图像
def getShrinkImg(img, scale=1.0):
    if 0.0 < scale < 1.0:
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    else:
        return img


#################################################
# 将图像转化为方形图
def get_square_img(img, Flag=False):
    if Flag:
        h, w, _ = img.shape
        if h > w:
            d = h - w
            img = img[round(d / 2 + 0.1):round(h - d / 2), :, :]
        elif w > h:
            d = w - h
            img = img[:, round(d / 2 + 0.1):round(w - d / 2), :]
    return img


# 使用生成器，减少内存占用
def img_generator(img_files, scale=1.0):
    for i in range(len(img_files)):
        img = cv2.imread(img_files[i])
        img = get_square_img(img, Flag=True)
        img = getShrinkImg(img, scale=scale)  # 压缩图片
        yield img


#################################################

def getTransformMatrix(origImg, origImg_name, transImg, transImg_name):
    # 自适应缩放待处理图像，减少处理开销
    shrink_scale = 1500.0 / ((transImg.shape[0] * transImg.shape[1]) ** 0.5)
    shrink_scale = 1.0 if shrink_scale > 1.0 else shrink_scale
    origImg = getShrinkImg(origImg, scale=shrink_scale)
    transImg = getShrinkImg(transImg, scale=shrink_scale)

    origImgGray = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    transImgGray = cv2.cvtColor(transImg, cv2.COLOR_BGR2GRAY)

    ############################################################

    # SIFT和SURF特征提取算法
    # sift = cv2.xfeatures2d_SIFT().create()   # find the keypoints and descriptors with SIFT
    # kp_orig, des_orig = sift.detectAndCompute(origImgGray, None)
    # kp_trans, des_trans = sift.detectAndCompute(transImgGray, None)

    hessian = 800
    surf = cv2.xfeatures2d.SURF_create(hessian)  # 将Hessian Threshold设置为500,阈值越大能检测的特征就越少
    kp_orig, des_orig = surf.detectAndCompute(origImgGray, None)
    kp_trans, des_trans = surf.detectAndCompute(transImgGray, None)

    ############################################################

    ############################################################
    # FLANN parameters (for SIFT and SURF)
    '''
    /* Nearest neighbour index algorithms */
    enum flann_algorithm_t
    {
        FLANN_INDEX_LINEAR = 0,
        FLANN_INDEX_KDTREE = 1,
        FLANN_INDEX_KMEANS = 2,
        FLANN_INDEX_COMPOSITE = 3,
        FLANN_INDEX_KDTREE_SINGLE = 4,
        FLANN_INDEX_HIERARCHICAL = 5,
        FLANN_INDEX_LSH = 6,
        FLANN_INDEX_SAVED = 254,
        FLANN_INDEX_AUTOTUNED = 255,

        // deprecated constants, should use the FLANN_INDEX_* ones instead
        LINEAR = 0,
        KDTREE = 1,
        KMEANS = 2,
        COMPOSITE = 3,
        KDTREE_SINGLE = 4,
        SAVED = 254,
        AUTOTUNED = 255
    };
    '''
    FLANN_INDEX_KMEANS = 2
    index_params = dict(algorithm=FLANN_INDEX_KMEANS, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_trans, des_orig, k=2)

    good_pts = [m for (m, n) in matches if m.distance < 0.7 * n.distance]

    ############################################################

    ############################################################
    # ORB和AKAZE特征提取算法
    """
    #orb = cv2.ORB_create()
    #kp_orig, des_orig = orb.detectAndCompute(origImgGray,None)
    #kp_trans, des_trans = orb.detectAndCompute(transImgGray,None)
    
    akaze = cv2.AKAZE_create()
    kp_orig, des_orig = akaze.detectAndCompute(origImgGray,None)
    kp_trans, des_trans = akaze.detectAndCompute(transImgGray,None)
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck = True)  # Brute Force Matcher（暴力匹配法）
    matches = bf.match(des_trans,des_orig)
    good_pts = matches
    """
    ############################################################

    MIN_MATCH_COUNT = 10
    if len(good_pts) > MIN_MATCH_COUNT:
        trans_pts = np.float32([kp_trans[m.queryIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        orig_pts = np.float32([kp_orig[m.trainIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        # 两种算法可选：cv2.LMEDS or cv2.RANSAC
        perArr, mask = cv2.findHomography(trans_pts / shrink_scale, orig_pts / shrink_scale, cv2.RANSAC, 5.0)
    else:
        assert False, "The two images <{}, {}> need {} points at least, but only match {} points." \
            .format(origImg_name, transImg_name, MIN_MATCH_COUNT, len(good_pts))
    return np.array(perArr)


def getPerArrsAndShapes(img_files, img_names, scale=1.0):
    assert len(img_files) >= 2, "need two images at least."
    count = 0
    perArrs = []
    Shapes = []
    src_img = None
    for img in img_generator(img_files, scale):
        if count > 0:
            matrix = getTransformMatrix(src_img, img_names[count - 1], img, img_names[count])
            perArrs.append(matrix)
        src_img = img.copy()
        Shapes.append(src_img.shape)
        count += 1
    return perArrs, Shapes


def PerArrs_Mutiply(perArrs, iters):
    assert len(perArrs) >= iters, "perspective array list must great than iteration number."
    Arr = np.eye(3, dtype=np.float32)
    for i in range(iters):
        Arr = np.dot(Arr, perArrs[i])
    return Arr


def getBoundary(shape, perArr):
    h, w = shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, perArr)
    bound_maxVal = np.max(dst, axis=0)
    bound_minVal = np.min(dst, axis=0)
    left_bound, right_bound = round(bound_minVal[0][0]), round(bound_maxVal[0][0])
    top_bound, bottom_bound = round(bound_minVal[0][1]), round(bound_maxVal[0][1])
    return int(left_bound), int(top_bound), int(right_bound), int(bottom_bound)


def getMaxBoundary(perArrs, Shapes):
    min_left_bound = min_top_bound = 0
    max_right_bound = Shapes[0][1] - 1
    max_bottom_bound = Shapes[0][0] - 1

    for i in range(len(Shapes)):
        arr = PerArrs_Mutiply(perArrs, i)
        left_bound, top_bound, right_bound, bottom_bound = getBoundary(Shapes[i], arr)

        min_left_bound = min(min_left_bound, left_bound)
        min_top_bound = min(min_top_bound, top_bound)
        max_right_bound = max(max_right_bound, right_bound)
        max_bottom_bound = max(max_bottom_bound, bottom_bound)

    return min_left_bound, min_top_bound, max_right_bound, max_bottom_bound


############################################################
# 最简明的拼接，利用掩模对图像重叠区进行融合操作，权重各0.5，拼接效果一般，但效率很高。
# alpha,beta分别为img1，img2的权重值
def getOverlayImg(img1, alpha, img2, beta):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY)

    mask_overlay = cv2.bitwise_and(mask1, mask2)
    mask_unoverlay = cv2.bitwise_not(mask_overlay)

    img_overlay = cv2.addWeighted(img1, alpha, img2, beta, gamma=0)
    img_overlay = cv2.bitwise_and(img_overlay, img_overlay, mask=mask_overlay)
    img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    img_merged = cv2.add(img_overlay, img_unoverlay)
    return img_merged


############################################################

def findMaxAreaContour(contours):  # 找出面积最大的封闭区域，暂未使用。
    contours_area = [cv2.contourArea(contours[i]) for i in range(len(contours))]
    max_area_contour = contours[contours_area.index(max(contours_area))]
    return [max_area_contour]


############################################################
# 重叠区利用掩模按列来进行图像的过渡融合，以水平*和*垂直距离来设置权重alpha，使重叠区过渡相对自然
def getOverlayImg_Distance(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY)

    mask_overlay = cv2.bitwise_and(mask1, mask2)
    mask_unoverlay = cv2.bitwise_not(mask_overlay)

    # 获取待拼接图像掩模的轮廓
    _, contours_dst, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    assert len(contours_dst) == 1

    # 计算待拼接图像的矩和中心
    M_dst = cv2.moments(contours_dst[0])
    cX_dst = round(M_dst["m10"] / M_dst["m00"])
    cY_dst = round(M_dst["m01"] / M_dst["m00"])

    # 获取重叠区掩模的轮廓
    _, contours_overlay, _ = cv2.findContours(mask_overlay, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # ** ** ** ** ** 利用重叠区域面积比来判断是否需要跳过当前图像的拼接 ** ** ** ** **
    # 重叠区域过大的拼接，不仅意义不大，反而影响拼接效果
    area_threshold = 0.5
    dst_area = cv2.contourArea(contours_dst[0])
    for k in range(len(contours_overlay)):
        if cv2.contourArea(contours_overlay[k]) / dst_area > area_threshold:
            print("Warning: 因重叠区域占比较大，跳过本次拼接！")
            return img1
    # ** ** ** ** ** 利用重叠区域面积比来判断是否需要跳过当前图像的拼接 ** ** ** ** **

    img_overlay = np.zeros_like(img1, np.uint8)
    for k in range(len(contours_overlay)):
        # 计算重叠区的矩和中心
        M_overlay = cv2.moments(contours_overlay[k])
        cX_overlay = round(M_overlay["m10"] / M_overlay["m00"])
        cY_overlay = round(M_overlay["m01"] / M_overlay["m00"])

        x, y, w, h = cv2.boundingRect(contours_overlay[k])
        img1_segment = np.copy(img1[y:y + h, x:x + w])
        img2_segment = np.copy(img2[y:y + h, x:x + w])

        img_col = np.zeros_like(img1_segment, np.uint8)
        if cX_dst >= cX_overlay:
            # print("重叠区从左向右拼接融合")
            for j in range(w):
                alpha = (w - j) / float(w)
                img_col[:, j:j + 1] = getOverlayImg(img1_segment[:, j:j + 1], alpha, img2_segment[:, j:j + 1], 1 - alpha)
        else:
            # print("重叠区从右向左拼接融合")
            for j in range(w):
                alpha = j / float(w)
                img_col[:, j:j + 1] = getOverlayImg(img1_segment[:, j:j + 1], alpha, img2_segment[:, j:j + 1], 1 - alpha)

        img_row = np.zeros_like(img1_segment, np.uint8)
        if cY_dst >= cY_overlay:
            # print("重叠区从上向下拼接融合")
            for i in range(h):
                alpha = (h - i) / float(h)
                img_row[i:i + 1, :] = getOverlayImg(img1_segment[i:i + 1, :], alpha, img2_segment[i:i + 1, :], 1 - alpha)
        else:
            # print("重叠区从下向上拼接融合")
            for i in range(h):
                alpha = i / float(h)
                img_row[i:i + 1, :] = getOverlayImg(img1_segment[i:i + 1, :], alpha, img2_segment[i:i + 1, :], 1 - alpha)

        img_segment = np.zeros_like(img_overlay, np.uint8)
        img_segment[y:y + h, x:x + w] = cv2.addWeighted(img_col, h / float(w + h), img_row, w / float(w + h), gamma=0)
        img_overlay = cv2.add(img_overlay, img_segment, mask=mask_overlay)

    img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    img_merged = cv2.add(img_overlay, img_unoverlay)
    # img_merged = cv2.polylines(img_merged, [contours_overlay[0]], True, (0,0,255), 5)   # 添加绘制重叠区域的框线
    return img_merged


############################################################


############################################################
# 最佳缝合线拼接
@jit(nopython=True)
def overlapImgExtend(img, direction):  # 本函数在此未使用
    # 填充重叠区黑边, 注意*本函数会直接操作输入图像*
    if direction == "LEFT_RIGHT":
        for x in range(img.shape[1]):
            for y in range(0, img.shape[0]):
                if img[y, x].all():
                    img[0:y, x] = img[y, x].copy()
                    break
            for y in range(img.shape[0] - 1, -1, -1):
                if img[y, x].all():
                    img[y + 1:img.shape[0], x] = img[y, x].copy()
                    break
    elif direction == "UP_DOWN":
        for y in range(img.shape[0]):
            for x in range(0, img.shape[1]):
                if img[y, x].all():
                    img[y, 0:x] = img[y, x].copy()
                    break
            for x in range(img.shape[1] - 1, -1, -1):
                if img[y, x].all():
                    img[y, x + 1:img.shape[1]] = img[y, x].copy()
                    break
    else:
        assert False, "wrong direction"
    return img


# 计算能量图方法v0
def calc_energy_v0(img):
    # 基于Sobel算子
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # 将它从2D滤波转换为3D滤波器
    # 为每个通道：R，G，B复制相同的滤波器
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # 将它从2D滤波转换为3D滤波器
    # 为每个通道：R，G，B复制相同的滤波器
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype(np.float32)
    convolved = np.absolute(fil_convolve(img, filter_du)) + np.absolute(fil_convolve(img, filter_dv))

    # 计算红，绿，蓝通道中的能量值之和
    energy_map = convolved.sum(axis=2)
    return energy_map


# 计算能量图方法v1 (与calc_energy_v0类似)
def calc_energy_v1(img):
    # 基于Sobel算子
    # grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    # grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    # convolved = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))

    # 基于Scharr算子 （优于Sobel算子）
    grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=-1)
    grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=-1)
    convolved = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))

    # 基于Laplacian算子 （二阶算子）
    # convolved = np.absolute(cv2.Laplacian(img, cv2.CV_32F, ksize=3))

    energy_map = convolved.sum(axis=2)
    return energy_map


# 计算能量图方法v2
def calc_energy_v2(img1, img2):
    """计算能量函数：灰度差分图和纹理权重图"""
    w_gray, w_grad = 0.1, 0.9
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 灰度差分图（亮度差异图）
    gray_dif = cv2.absdiff(np.float32(gray1), np.float32(gray2))
    gray_dif = cv2.normalize(gray_dif, None, 0, 255, cv2.NORM_MINMAX)

    # 梯度差分图（纹理结构差异图）
    grad_x = cv2.Sobel(gray_dif, cv2.CV_32F, 1, 0, ksize=-1)
    grad_y = cv2.Sobel(gray_dif, cv2.CV_32F, 0, 1, ksize=-1)
    grad_dif = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))
    # grad_dif = np.absolute(cv2.Laplacian(gray_dif, cv2.CV_32F, ksize=3))  # 基于Laplacian算子
    grad_dif = cv2.normalize(grad_dif, None, 0, 255, cv2.NORM_MINMAX)

    # 此处卷积核实质是对相邻8个像素求和
    kernel = np.ones([3, 3], dtype=np.float32)
    kernel[1, 1] = 0

    # 亮度和纹理权重图
    weights_gray = sig_convolve(gray_dif, kernel, "same") / 8.0
    weights_grad = sig_convolve(grad_dif, kernel, "same") / 8.0

    # 能量图
    weights = w_gray * weights_gray + w_grad * weights_grad
    energy = np.multiply(grad_dif, weights/255.0)
    # energy = w_gray * gray_dif + w_grad * grad_dif    # 跳过亮度和纹理权重图步骤，简化计算量
    return energy


def minimum_seam(imgs, direction):
    row, col, _ = imgs[0].shape
    if len(imgs) == 1:
        energy_map = calc_energy_v1(imgs[0])
    elif len(imgs) == 2:
        energy_map = calc_energy_v2(imgs[0], imgs[1])
    else:
        assert False, "ERROR: 计算能量图的输入图片有误（只允1或2张）"
    backtrack = np.zeros_like(energy_map, dtype=np.int32)

    @jit(nopython=True)
    def cal_backtrack(row, col, energy_map, backtrack):
        min_energy = 0
        if direction == "LEFT_RIGHT":
            for i in range(1, row):
                for j in range(0, col):
                    # 处理图像的左侧边缘，确保不会索引-1
                    if j == 0:
                        idx = np.argmin(energy_map[i - 1, j:j + 2])
                        backtrack[i, j] = idx + j
                        min_energy = energy_map[i - 1, idx + j]
                    else:
                        idx = np.argmin(energy_map[i - 1, j - 1:j + 2])
                        backtrack[i, j] = idx + j - 1
                        min_energy = energy_map[i - 1, idx + j - 1]
                    energy_map[i, j] += min_energy
        elif direction == "UP_DOWN":
            for j in range(1, col):
                for i in range(0, row):
                    # 处理图像的上侧边缘，确保不会索引-1
                    if i == 0:
                        idy = np.argmin(energy_map[i:i + 2, j - 1])
                        backtrack[i, j] = idy + i
                        min_energy = energy_map[idy + i, j - 1]
                    else:
                        idy = np.argmin(energy_map[i - 1:i + 2, j - 1])
                        backtrack[i, j] = idy + i - 1
                        min_energy = energy_map[idy + i - 1, j - 1]
                    energy_map[i, j] += min_energy
        else:
            assert False, "wrong direction"
        return energy_map, backtrack

    return cal_backtrack(row, col, energy_map, backtrack)


# 求取包含缝合线渐变区域的权重矩阵
def get_seam_weight(seam_pts, shape, direction, mix_width=10):
    weight_array = [np.zeros(shape, np.uint8) for i in range(mix_width)]
    for i in range(mix_width):
        cv2.polylines(weight_array[i], [seam_pts], isClosed=False, color=1, thickness=i + 1)
    weight_array = np.sum(weight_array, axis=0) / 2.0 / mix_width

    @jit(nopython=True)
    def fill_half_weight(weight_array, direction, shape):
        if direction == "LEFT_RIGHT":
            for i in range(shape[0]):
                for j in range(0, shape[1]):
                    if abs(weight_array[i][j] - 0.5) < 1e-4:
                        break
                    weight_array[i][j] = 1.0 - weight_array[i][j]
        elif direction == "UP_DOWN":
            for j in range(shape[1]):
                for i in range(0, shape[0]):
                    if abs(weight_array[i][j] - 0.5) < 1e-4:
                        break
                    weight_array[i][j] = 1.0 - weight_array[i][j]
        else:
            assert False, "wrong direction"
        return weight_array

    return fill_half_weight(weight_array, direction, shape)


def find_seam(img_segments, direction):
    # 自适应缩放待处理图像，减少处理开销
    shrink_scale = 1500.0 / ((img_segments[0].shape[0] * img_segments[0].shape[1]) ** 0.5)
    shrink_scale = 1.0 if shrink_scale > 1.0 else shrink_scale
    img_segments[0] = getShrinkImg(img_segments[0], scale=shrink_scale)
    if len(img_segments) > 1:  # 用于计算能量图方法v2
        img_segments[1] = getShrinkImg(img_segments[1], scale=shrink_scale)

    energy_map, backtrack = minimum_seam(img_segments, direction)
    row, col, _ = img_segments[0].shape

    @jit(nopython=True)
    def search_seam_pts(energy_map, backtrack, direction, row, col):
        seam_pts = []
        if direction == "LEFT_RIGHT":
            # 限制缝合线搜索起始位置位于图像（1/3:2/3）的中间区域
            j = np.argmin(energy_map[-1, int(col / 3.0):int(2 * col / 3.0)])
            for i in range(row - 1, -1, -1):
                seam_pts.append([j, i])
                j = backtrack[i, j]
        elif direction == "UP_DOWN":
            # 限制缝合线搜索起始位置位于图像（1/3:2/3）的中间区域
            i = np.argmin(energy_map[int(row / 3.0):int(2 * row / 3.0), -1])
            for j in range(col - 1, -1, -1):
                seam_pts.append([j, i])
                i = backtrack[i, j]
        else:
            assert False, "wrong direction"
        return seam_pts

    seam_pts = search_seam_pts(energy_map, backtrack, direction, row, col)
    seam_pts = np.array(seam_pts, np.float32).reshape((-1, 2)) / shrink_scale
    seam_pts = seam_pts.astype(np.int32)
    return seam_pts


def getOverlayImg_Seam(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY)

    mask_overlay = cv2.bitwise_and(mask1, mask2)
    mask_unoverlay = cv2.bitwise_not(mask_overlay)
    mix_width = 10  # 缝合线区域的融合宽度

    # 获取待拼接图像掩模的轮廓
    _, contours_dst, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    assert len(contours_dst) == 1

    # 计算待拼接图像的矩和中心
    M_dst = cv2.moments(contours_dst[0])
    cX_dst = round(M_dst["m10"] / M_dst["m00"])
    cY_dst = round(M_dst["m01"] / M_dst["m00"])

    # 获取重叠区掩模的轮廓
    _, contours_overlay, _ = cv2.findContours(mask_overlay, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ** ** ** ** ** 利用重叠区域面积比来判断是否需要跳过当前图像的拼接 ** ** ** ** **
    # 重叠区域过大的拼接，不仅意义不大，反而影响拼接效果
    area_threshold = 0.75
    dst_area = cv2.contourArea(contours_dst[0])
    for k in range(len(contours_overlay)):
        if cv2.contourArea(contours_overlay[k]) / dst_area >= area_threshold:
            print("Warning: 因重叠区域占比较大，跳过本次图像拼接！")
            return img1
    # ** ** ** ** ** 利用重叠区域面积比来判断是否需要跳过当前图像的拼接 ** ** ** ** **

    ############# 用于计算能量图方法v1的合并图 #############
    # img_overlay = cv2.addWeighted(img1, 0.5, img2, 0.5, gamma=0)
    # img_overlay = cv2.bitwise_and(img_overlay, img_overlay, mask=mask_overlay)
    # img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    # img_for_energy = cv2.add(img_overlay, img_unoverlay)
    ##############################################

    img_overlay = np.zeros_like(img1, np.uint8)
    for k in range(len(contours_overlay)):
        # 计算重叠区的矩和中心
        M_overlay = cv2.moments(contours_overlay[k])
        cX_overlay = round(M_overlay["m10"] / M_overlay["m00"])
        cY_overlay = round(M_overlay["m01"] / M_overlay["m00"])

        # TODO: 拐角可以考虑水平和垂直方向上缝合线的叠加
        x, y, w, h = cv2.boundingRect(contours_overlay[k])
        if abs(cX_dst - cX_overlay) >= abs(cY_dst - cY_overlay):
            direction = "LEFT_RIGHT"
            # seam_pts = find_seam([img_for_energy[y:y + h, x:x + w]], direction)  #计算能量图方法v1
            seam_pts = find_seam([img1[y:y + h, x:x + w], img2[y:y + h, x:x + w]], direction)  # 计算能量图方法v2
            if cX_dst >= cX_overlay:
                # print("重叠区从左向右拼接融合")
                weight_array1 = get_seam_weight(seam_pts, (h, w), direction, mix_width)
                weight_array2 = 1.0 - weight_array1
            else:
                # print("重叠区从右向左拼接融合")
                weight_array2 = get_seam_weight(seam_pts, (h, w), direction, mix_width)
                weight_array1 = 1.0 - weight_array2
        else:
            direction = "UP_DOWN"
            # seam_pts = find_seam([img_for_energy[y:y + h, x:x + w]], direction)  #计算能量图方法v1
            seam_pts = find_seam([img1[y:y + h, x:x + w], img2[y:y + h, x:x + w]], direction)  # 计算能量图方法v2
            if cY_dst >= cY_overlay:
                # print("重叠区从上向下拼接融合")
                weight_array1 = get_seam_weight(seam_pts, (h, w), direction, mix_width)
                weight_array2 = 1.0 - weight_array1
            else:
                # print("重叠区从下向上拼接融合")
                weight_array2 = get_seam_weight(seam_pts, (h, w), direction, mix_width)
                weight_array1 = 1.0 - weight_array2
        weighted_img1_sement = (img1[y:y + h, x:x + w] * np.stack([weight_array1] * 3, axis=2)).astype(np.uint8)
        weighted_img2_sement = (img2[y:y + h, x:x + w] * np.stack([weight_array2] * 3, axis=2)).astype(np.uint8)
        img_segment = np.zeros_like(img_overlay, np.uint8)
        img_segment[y:y + h, x:x + w] = cv2.add(weighted_img1_sement, weighted_img2_sement)
        img_overlay = cv2.add(img_overlay, img_segment, mask=mask_overlay)

        ################################################
        # 绘制缝合线
        # img_overlay[y:y + h, x:x + w] = cv2.polylines(img_overlay[y:y + h, x:x + w], [seam_pts], False, (0, 0, 255), 10)
        ################################################

    img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    img_merged = cv2.add(img_overlay, img_unoverlay)
    return img_merged


############################################################

def Show_Img(img, title="", lastFlag=False):  # 直接绘制图像，用于调试
    if len(img.shape) == 3:
        # OpenCV is BGR, but Matplotlib is RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        assert False, "Can't show image!"

    plt.figure(num=title)
    plt.imshow(img)
    plt.axis("off")
    if lastFlag:
        plt.show()
    return None


# Processing one by one
def getMosiacImage(read_path, save_path="./", suffix=".jpg", isShowImg=False, isSaveImg=False):
    img_files, img_names = getImgList(read_path, suffix, reverse=False)  # 获取指定文件夹下的指定后缀名的图像文件
    assert len(img_files) >= 2, "need two images at least."
    #####################
    # 以下参数仅用于快速测试
    img_files = img_files[0:4]
    scale = 1.0
    #####################

    mergeImg = None  # 用于保存当前拼接的图像
    priorImg = None  # 用于保存生成器产生的前一张图像
    count = 0
    PerArrs = []
    Shapes = []
    priorArrs = [np.eye(3, dtype=np.float32)]
    for img in img_generator(img_files, scale):
        if count > 0:
            per_arr = getTransformMatrix(priorImg, img_names[count - 1], img, img_names[count])
            PerArrs.append(per_arr)
            Shapes.append(img.shape)
            min_left_bound, min_top_bound, max_right_bound, max_bottom_bound = getMaxBoundary(PerArrs,
                                                                                              Shapes)  # 获取拼接图像的最大边界
            new_width, new_height = (
                max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

            # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
            src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                                   [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
            dst_rect = np.float32(
                [[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1], [new_width - 1, 0]]).reshape(-1, 1, 2)
            transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)

            #################################################################################
            # 当前已拼接图的平移
            perArr = PerArrs_Mutiply(np.linalg.inv(priorArrs), count)  # 利用求逆矩阵恢复到第一张基准图的原始坐标
            perArr = np.dot(transArr, perArr)  ## 计算平移时的新透射变换矩阵
            mergeImg = cv2.warpPerspective(mergeImg, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)
            priorArrs.append(perArr)
            #################################################################################

            perArr = PerArrs_Mutiply(PerArrs, count)  # 透射变换矩阵的叠加连乘
            perArr = np.dot(transArr, perArr)  # 计算平移时的透射变换矩阵

            # 可选cv2.INTER_LINEAR，但可能会出现黑色边缘锯齿
            # 使用cv2.WARP_INVERSE_MAP，则要求逆矩阵np.linalg.inv(perArr)
            warpImg = cv2.warpPerspective(img, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)

            ############################################################################
            # 通过调用getOverlayImg、getOverlayImg_Distance或getgetOverlayImg_Seam函数实现连续拼接
            # mergeImg = getOverlayImg(mergeImg, 0.5, warpImg, 0.5)  # 重叠区各取50%，过渡不自然
            mergeImg = getOverlayImg_Distance(mergeImg, warpImg)  # 按距离设置权重，过渡相对自然
            # mergeImg = getOverlayImg_Seam(mergeImg, warpImg)  # 最佳缝合线拼接
            ############################################################################

            if isShowImg:
                Show_Img(cv2.medianBlur(mergeImg, 3), title="Merged Image" + str(count), lastFlag=True)
                # cv2.imwrite(save_path + "merge_img" + str(count) + suffix, cv2.medianBlur(mergeImg, 3))  # 保存拼接后的图像
        else:
            mergeImg = np.copy(img)
            Shapes.append(img.shape)

        priorImg = np.copy(img)
        count += 1

    if isSaveImg:
        cv2.imwrite(save_path + "merged_img" + suffix, cv2.medianBlur(mergeImg, 3))  # 保存拼接图像
    return mergeImg


if __name__ == '__main__':
    # getReducedImages(read_path="../CV2_LEARN/Aerial_Images/Original_Image_Set/",
    #                 save_path="../CV2_LEARN/Aerial_Images/New_Image_Set/", suffix=".JPG")
    mergeImg = getMosiacImage(read_path="../CV2_LEARN/Aerial_Images/Original_Image_Set/",
                              save_path="../CV2_LEARN/Aerial_Images/", suffix=".JPG", isShowImg=False, isSaveImg=True)
