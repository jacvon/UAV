import os
import shutil
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import convolve
from numba import jit


###剔除重叠冗余的图片###
def removeRedundantImgs(img_files, img_names, isResize=False, scale=0.5):
    PerArrs, Shapes = getPerArrsAndShapes(img_files, img_names, isResize, scale)

    index = 1
    removed_indexs = []
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
        _, contours01, _ = cv2.findContours(np.copy(img01_mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        assert len(contours01) == 1, "the two images must have only one overlay area."

        area01 = cv2.contourArea(contours01[0])
        ratio01 = area01 / area0
        assert ratio01 > 0.2, "The overlap of the two images <{}, {}> is less than 20% <{:.1%}>." \
            .format(img_names[index - 1], img_names[index], ratio01)

        h, w = Shapes[index + 1][0:2]
        pts2 = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst12 = cv2.perspectiveTransform(pts2, PerArrs[index])
        img12_mask = cv2.fillPoly(img1.copy(), [np.int32(dst12)], 255)
        _, contours12, _ = cv2.findContours(np.copy(img12_mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        assert len(contours12) == 1, "the two images must have only one overlay area."

        area12 = cv2.contourArea(contours12[0])
        ratio12 = area12 / area1
        assert ratio12 > 0.2, "The overlap of the two images <{}, {}> is less than 20% <{:.1%}>." \
            .format(img_names[index], img_names[index + 1], ratio12)

        dst02 = cv2.perspectiveTransform(pts2, np.dot(PerArrs[index - 1], PerArrs[index]))
        img02_mask = cv2.fillPoly(img0.copy(), [np.int32(dst02)], 255)
        _, contours02, _ = cv2.findContours(np.copy(img02_mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

    ################
    # 使用以下参数进行图片压缩，可减少计算量。
    isResize = True
    scale = 0.25
    ################

    while True:
        img_num = len(img_files)
        img_files, img_names = removeRedundantImgs(img_files, img_names, isResize, scale)
        if img_num == len(img_files):
            break

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


#################################################
# 将图像转化为方形图
def get_square_img(img):
    h, w, _ = img.shape
    if h > w:
        d = h - w
        img = img[round(d / 2 + 0.1):round(h - d / 2), :, :]
    elif w > h:
        d = w - h
        img = img[:, round(d / 2 + 0.1):round(w - d / 2), :]
    return img


# 使用生成器，减少内存占用
def img_generator(img_files, isResize=False, scale=0.5):
    for i in range(len(img_files)):
        img = cv2.imread(img_files[i])
        img = get_square_img(img)
        if isResize:
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)  # 压缩图片
        yield img


#################################################

def getTransformMatrix(origImg, origImg_name, transImg, transImg_name):
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
    perArr = None
    MIN_MATCH_COUNT = 20
    if len(good_pts) > MIN_MATCH_COUNT:
        trans_pts = np.float32([kp_trans[m.queryIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        orig_pts = np.float32([kp_orig[m.trainIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        # 两种算法可选：cv2.LMEDS or cv2.RANSAC
        perArr, mask = cv2.findHomography(trans_pts, orig_pts, cv2.RANSAC, 5.0)
    else:
        assert False, "The two images <{}, {}> need {} points at least, but only match {} points." \
            .format(origImg_name, transImg_name, MIN_MATCH_COUNT, len(good_pts))
    return np.array(perArr)


def getPerArrsAndShapes(img_files, img_names, isResize=False, scale=0.5):
    assert len(img_files) >= 2, "need two images at least."
    count = 0
    perArrs = []
    Shapes = []
    src_img = None
    for img in img_generator(img_files, isResize, scale):
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
    _, mask1 = cv2.threshold(img1_gray, 1, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 1, 255, cv2.THRESH_BINARY)

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
    _, mask1 = cv2.threshold(img1_gray, 1, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 1, 255, cv2.THRESH_BINARY)

    mask_overlay = cv2.bitwise_and(mask1, mask2)
    mask_unoverlay = cv2.bitwise_not(mask_overlay)

    # 获取待拼接图像掩模的轮廓
    _, contours_dst, _ = cv2.findContours(np.copy(mask2), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    assert len(contours_dst) == 1

    # 计算待拼接图像的矩和中心
    M_dst = cv2.moments(contours_dst[0])
    cX_dst = round(M_dst["m10"] / M_dst["m00"])
    cY_dst = round(M_dst["m01"] / M_dst["m00"])

    # 获取重叠区掩模的轮廓
    _, contours_overlay, _ = cv2.findContours(np.copy(mask_overlay),
                                              cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_overlay = np.zeros_like(img1, np.uint8)
    for k in range(len(contours_overlay)):
        # 计算重叠区的矩和中心
        M_overlay = cv2.moments(contours_overlay[k])
        cX_overlay = round(M_overlay["m10"] / M_overlay["m00"])
        cY_overlay = round(M_overlay["m01"] / M_overlay["m00"])

        # 计算重叠区的边界极值
        bound_maxVal = np.max(contours_overlay[k], axis=0)
        bound_minVal = np.min(contours_overlay[k], axis=0)
        dx = bound_maxVal[0, 0] - bound_minVal[0, 0]
        dy = bound_maxVal[0, 1] - bound_minVal[0, 1]

        mask_segment = cv2.fillPoly(np.zeros(img1.shape[0:2], np.uint8), [contours_overlay[k]], 255)
        img_col = np.zeros_like(img1, np.uint8)
        d = bound_maxVal[0, 0] - bound_minVal[0, 0] + 1
        if cX_dst >= cX_overlay:
            # print("重叠区向右拼接融合")
            for j in range(bound_minVal[0, 0], bound_maxVal[0, 0] + 1):
                alpha = (bound_maxVal[0, 0] + 1 - j) / d
                img_col[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1] = \
                    getOverlayImg(img1[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1], alpha,
                                  img2[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1], 1 - alpha)
        else:
            # print("重叠区向左拼接融合")
            for j in range(bound_minVal[0, 0], bound_maxVal[0, 0] + 1):
                alpha = (j - bound_minVal[0, 0]) / d
                img_col[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1] = \
                    getOverlayImg(img1[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1], alpha,
                                  img2[bound_minVal[0, 1]:bound_maxVal[0, 1] + 1, j:j + 1], 1 - alpha)

        img_row = np.zeros_like(img1, np.uint8)
        d = bound_maxVal[0, 1] - bound_minVal[0, 1] + 1
        if cY_dst >= cY_overlay:
            # print("重叠区向下拼接融合")
            for i in range(bound_minVal[0, 1], bound_maxVal[0, 1] + 1):
                alpha = (bound_maxVal[0, 1] + 1 - i) / d
                img_row[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1] = \
                    getOverlayImg(img1[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1], alpha,
                                  img2[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1], 1 - alpha)
        else:
            # print("重叠区向上拼接融合")
            for i in range(bound_minVal[0, 1], bound_maxVal[0, 1] + 1):
                alpha = (i - bound_minVal[0, 1]) / d
                img_row[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1] = \
                    getOverlayImg(img1[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1], alpha,
                                  img2[i:i + 1, bound_minVal[0, 0]:bound_maxVal[0, 0] + 1], 1 - alpha)

        img_segment = cv2.addWeighted(img_col, dy / float(dx + dy), img_row, dx / float(dx + dy), gamma=0)
        img_segment = cv2.bitwise_and(img_segment, img_segment, mask=mask_segment)
        img_overlay = cv2.add(img_overlay, img_segment, mask=mask_overlay)

    img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    img_merged = cv2.add(img_overlay, img_unoverlay)
    # img_merged = cv2.polylines(img_merged, [contours_overlay[0]], True, (0,0,255), 5)   # 添加绘制重叠区域的框线
    return img_merged


############################################################


############################################################
# 最佳缝合线拼接
@jit
def overlapImgExtend(img, direction):  # 填充重叠区黑边, 注意*本函数会直接操作输入图像*
    if direction == "VERTICAL":
        for x in range(img.shape[1]):
            for y in range(0, img.shape[0]):
                if img[y, x].all():
                    img[0:y, x] = img[y, x].copy()
                    break
            for y in range(img.shape[0] - 1, -1, -1):
                if img[y, x].all():
                    img[y + 1:img.shape[0], x] = img[y, x].copy()
                    break

    if direction == "HORIZONAL":
        for y in range(img.shape[0]):
            for x in range(0, img.shape[1]):
                if img[y, x].all():
                    img[y, 0:x] = img[y, x].copy()
                    break
            for x in range(img.shape[1] - 1, -1, -1):
                if img[y, x].all():
                    img[y, x + 1:img.shape[1]] = img[y, x].copy()
                    break
    return img


'''
def calc_energy(img): # c
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
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # 计算红，绿，蓝通道中的能量值之和
    energy_map = convolved.sum(axis=2)
    return energy_map
'''


def calc_energy(img):
    """
    # 基于Sobel算子
    grad_x=cv2.Sobel(img,cv2.CV_32F,1,0,ksize=3)
    grad_y=cv2.Sobel(img,cv2.CV_32F,0,1,ksize=3)
    convolved = np.sqrt(np.power(grad_x,2)+np.power(grad_y,2))
    """
    # 基于Scharr算子
    grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=-1)
    grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=-1)
    convolved = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))

    # convolved=np.absolute(cv2.Laplacian(img,cv2.CV_32F))

    energy_map = convolved.sum(axis=2)
    return energy_map


@jit
def minimum_seam(img, direction):
    row, col, _ = img.shape
    img_ext = overlapImgExtend(img.copy(), direction)
    energy_map = calc_energy(img_ext)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int32)

    min_energy = 0
    if direction == "VERTICAL":
        for i in range(1, row):
            for j in range(0, col):
                # 处理图像的左侧边缘，确保不会索引-1
                if j == 0:
                    idx = np.argmin(M[i - 1, j:j + 2])
                    backtrack[i, j] = idx + j
                    min_energy = M[i - 1, idx + j]
                else:
                    idx = np.argmin(M[i - 1, j - 1:j + 2])
                    backtrack[i, j] = idx + j - 1
                    min_energy = M[i - 1, idx + j - 1]
                M[i, j] += min_energy
    elif direction == "HORIZONAL":
        for j in range(1, col):
            for i in range(0, row):
                # 处理图像的上侧边缘，确保不会索引-1
                if i == 0:
                    idy = np.argmin(M[i:i + 2, j - 1])
                    backtrack[i, j] = idy + i
                    min_energy = M[idy + i, j - 1]
                else:
                    idy = np.argmin(M[i - 1:i + 2, j - 1])
                    backtrack[i, j] = idy + i - 1
                    min_energy = M[idy + i - 1, j - 1]
                M[i, j] += min_energy
    else:
        assert False, "wrong direction"

    return M, backtrack


def find_seam(img, bound_minVal, bound_maxVal, direction):
    left, right = bound_minVal[0][0], bound_maxVal[0][0]
    top, bottom = bound_minVal[0][1], bound_maxVal[0][1]

    pts0 = pts1 = pts2 = []
    row, col, _ = img[top:bottom, left:right].shape

    if direction == "RIGHT" or direction == "LEFT":
        M, backtrack = minimum_seam(img[top:bottom, left:right], direction="VERTICAL")

        j = np.argmin(M[-1])
        for i in reversed(range(row)):
            pts0.append([j + left, i + top])
            j = backtrack[i, j]

        pts1 = pts0.copy()
        pts1.extend([[right, top], [right, bottom]])
        pts2 = pts0.copy()
        pts2.extend([[left, top], [left, bottom]])
    elif direction == "DOWN" or direction == "UP":
        M, backtrack = minimum_seam(img[top:bottom, left:right], direction="HORIZONAL")

        i = np.argmin(M[-1])
        for j in reversed(range(col)):
            pts0.append([j + left, i + top])
            i = backtrack[i, j]

        pts1 = pts0.copy()
        pts1.extend([[left, bottom], [right, bottom]])
        pts2 = pts0.copy()
        pts2.extend([[left, top], [right, top]])
    else:
        assert False, "wrong direction"

    # 若拼接方向相反，两个点集进行交换
    if direction == "LEFT" or direction == "UP":
        pts1, pts2 = pts2.copy(), pts1.copy()

    pts0 = np.array(pts0, np.int32).reshape((-1, 1, 2))
    pts1 = np.array(pts1, np.int32).reshape((-1, 1, 2))
    pts2 = np.array(pts2, np.int32).reshape((-1, 1, 2))
    return pts0, pts1, pts2


def getOverlayImg_Seam(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(img1_gray, 1, 255, cv2.THRESH_BINARY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask2 = cv2.threshold(img2_gray, 1, 255, cv2.THRESH_BINARY)

    mask_overlay = cv2.bitwise_and(mask1, mask2)
    mask_unoverlay = cv2.bitwise_not(mask_overlay)

    # 获取待拼接图像掩模的轮廓
    _, contours_dst, _ = cv2.findContours(np.copy(mask2), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    assert len(contours_dst) == 1

    # 计算待拼接图像的矩和中心
    M_dst = cv2.moments(contours_dst[0])
    cX_dst = round(M_dst["m10"] / M_dst["m00"])
    cY_dst = round(M_dst["m01"] / M_dst["m00"])

    # 获取重叠区掩模的轮廓
    _, contours_overlay, _ = cv2.findContours(np.copy(mask_overlay), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_overlay = cv2.addWeighted(img1, 0.5, img2, 0.5, gamma=0)
    img_overlay = cv2.bitwise_and(img_overlay, img_overlay, mask=mask_overlay)
    img_unoverlay = cv2.add(img1, img2, mask=mask_unoverlay)
    img_merged = cv2.add(img_overlay, img_unoverlay)

    img_overlay = np.zeros_like(img1, np.uint8)
    for k in range(len(contours_overlay)):
        # 计算重叠区的矩和中心
        M_overlay = cv2.moments(contours_overlay[k])
        cX_overlay = round(M_overlay["m10"] / M_overlay["m00"])
        cY_overlay = round(M_overlay["m01"] / M_overlay["m00"])

        # 计算重叠区的边界极值
        bound_maxVal = np.max(contours_overlay[k], axis=0)
        bound_minVal = np.min(contours_overlay[k], axis=0)
        dx = bound_maxVal[0, 0] - bound_minVal[0, 0]
        dy = bound_maxVal[0, 1] - bound_minVal[0, 1]

        pts0 = pts1 = pts2 = None
        mask_segment = cv2.fillPoly(np.zeros(img1.shape[0:2], np.uint8), [contours_overlay[k]], 255)
        if dy >= dx:
            if cX_dst >= cX_overlay:
                # print("重叠区向右拼接融合")
                pts0, pts1, pts2 = find_seam(img_merged, bound_minVal, bound_maxVal, direction="RIGHT")
            else:
                # print("重叠区向左拼接融合")
                pts0, pts1, pts2 = find_seam(img_merged, bound_minVal, bound_maxVal, direction="LEFT")
        else:
            if cY_dst >= cY_overlay:
                # print("重叠区向下拼接融合")
                pts0, pts1, pts2 = find_seam(img_merged, bound_minVal, bound_maxVal, direction="DOWN")
            else:
                # print("重叠区向上拼接融合")
                pts0, pts1, pts2 = find_seam(img_merged, bound_minVal, bound_maxVal, direction="UP")

        img1_part = cv2.fillPoly(img1.copy(), [pts1], (0, 0, 0))
        img2_part = cv2.fillPoly(img2.copy(), [pts2], (0, 0, 0))

        # 填补接缝上缺失的像素点
        for i in range(len(pts0)):
            if img1[pts0[i][0][1], pts0[i][0][0]].all():
                img1_part[pts0[i][0][1], pts0[i][0][0]] = img1[pts0[i][0][1], pts0[i][0][0]].copy()
            else:
                img2_part[pts0[i][0][1], pts0[i][0][0]] = img2[pts0[i][0][1], pts0[i][0][0]].copy()

        img_segment = cv2.add(img1_part, img2_part, mask=mask_segment)
        img_overlay = cv2.add(img_overlay, img_segment, mask=mask_overlay)
        ################################################
        # 绘制缝合线，便于调试
        # img_overlay = cv2.polylines(img_overlay, [pts0], False, (0,0,255), 5)
        # img_overlay = cv2.polylines(img_overlay, [pts1], True, (0,0,255), 5)
        # img_overlay = cv2.polylines(img_overlay, [pts2], True, (0,0,255), 5)
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


# Batch Processing
def getMosiacImage(read_path, save_path="./", suffix=".jpg", isShowImg=False, isSaveImg=False):
    img_files, img_names = getImgList(read_path, suffix, reverse=False)  # 获取指定文件夹下的指定后缀名的图像文件
    assert len(img_files) >= 2, "need two images at least."
    #####################
    # 以下参数仅用于快速测试
    # img_files = img_files[0:3]
    isResize = True
    scale = 0.5
    #####################
    PerArrs, Shapes = getPerArrsAndShapes(img_files, img_names, isResize, scale)  # 获取变换矩阵列表
    min_left_bound, min_top_bound, max_right_bound, max_bottom_bound = getMaxBoundary(PerArrs, Shapes)  # 获取最终拼接图像的最大边界
    new_width, new_height = (max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

    # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
    src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                           [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
    dst_rect = np.float32([[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1], [new_width - 1, 0]]).reshape(
        -1, 1, 2)
    transArr = cv2.getPerspectiveTransform(src_rect, dst_rect)

    mergeImg = None  # 用于保存拼接后的图像
    count = 0
    for img in img_generator(img_files, isResize, scale):
        perArr = PerArrs_Mutiply(PerArrs, count)  # 透射变换矩阵的叠加连乘
        perArr = np.dot(transArr, perArr)  # 计算平移时的透射变换矩阵

        # 可选cv2.INTER_LINEAR，但可能会出现黑色边缘锯齿
        # 使用cv2.WARP_INVERSE_MAP，则要求逆矩阵np.linalg.inv(perArr)
        warpImg = cv2.warpPerspective(img, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)

        if isShowImg:
            Show_Img(warpImg, title="Transformed Img" + str(count))
            # cv2.imwrite(save_path + "trans_img" + str(count) + suffix, warpImg)  # 保存变换后的图像

        #######################################################################################################
        # 通过调用getOverlayImg、getOverlayImg_Distance或getOverlayImg_Seam函数实现连续拼接
        if count == 0:
            mergeImg = np.copy(warpImg)
        else:
            # mergeImg = getOverlayImg(mergeImg, 0.5, warpImg, 0.5)       # 重叠区各取50%，过渡不自然
            # mergeImg = getOverlayImg_Distance(mergeImg, warpImg)      # 按距离设置权重，过渡相对自然
            mergeImg = getOverlayImg_Seam(mergeImg, warpImg)  # 最佳缝合线拼接
        #######################################################################################################
        count += 1

    if isShowImg:
        Show_Img(mergeImg, title="Merged Image", lastFlag=True)
    if isSaveImg:
        cv2.imwrite(save_path + "merged_img" + suffix, mergeImg)  # 保存拼接图像
    return mergeImg


# Processing one by one
def getMosiacImageFlow(read_path, save_path="./", suffix=".jpg", isShowImg=False, isSaveImg=False):
    img_files, img_names = getImgList(read_path, suffix, reverse=False)  # 获取指定文件夹下的指定后缀名的图像文件
    assert len(img_files) >= 2, "need two images at least."
    #####################
    # 以下参数仅用于快速测试
    img_files = img_files[0:3]
    isResize = True
    scale = 0.5
    #####################

    mergeImg = None  # 用于保存当前拼接的图像
    priorImg = None  # 用于保存生成器产生的前一张图像
    count = 0
    PerArrs = []
    Shapes = []
    priorArrs = [np.eye(3, dtype=np.float32)]
    for img in img_generator(img_files, isResize, scale):
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
                                   [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1,
                                                                                                                   1, 2)
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
            # mergeImg = getOverlayImg(mergeImg, 0.5, warpImg, 0.5)       # 重叠区各取50%，过渡不自然
            # mergeImg = getOverlayImg_Distance(mergeImg, warpImg)      # 按距离设置权重，过渡相对自然
            mergeImg = getOverlayImg_Seam(mergeImg, warpImg)  # 最佳缝合线拼接
            ############################################################################

            if isShowImg:
                Show_Img(mergeImg, title="Merged Image" + str(count), lastFlag=True)
                # cv2.imwrite(save_path + "merge_img" + str(count) + suffix, mergeImg)  # 保存拼接后的图像
        else:
            mergeImg = np.copy(img)
            Shapes.append(img.shape)

        priorImg = np.copy(img)
        count += 1

    if isSaveImg:
        cv2.imwrite(save_path + "merged_img" + suffix, mergeImg)  # 保存拼接图像
    return mergeImg


if __name__ == '__main__':
    getReducedImages(read_path="../CV2_LEARN/Aerial_Images/Original_Image_Set/",
                     save_path="../CV2_LEARN/Aerial_Images/New_Image_Set/", suffix=".JPG")
    # mergeImg = getMosiacImage(read_path = "../CV2_LEARN/Aerial_Images/New_Image_Set/",
    #                          save_path = "../CV2_LEARN/Aerial_Images/", suffix = ".JPG",isShowImg = False, isSaveImg = True)
    # mergeImg = getMosiacImageFlow(read_path = "../CV2_LEARN/Aerial_Images/New_Image_Set/",
    #                              save_path = "../CV2_LEARN/Aerial_Images/", suffix = ".JPG",isShowImg = False, isSaveImg = True)
