import cv2  # opencv-python==3.4.2.16, opencv-contrib-python==3.4.2.16
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim
import os
import pyexiv2
from geographiclib.geodesic import Geodesic
import time
import csv
from scipy import interpolate
from numba import jit
import compare.image_similarity_model as ism


def getTransformMatrix(origImg, transImg, transImg_name):
    # 自适应缩放待处理图像，减少处理开销
    shrink_scale = 1000.0 / ((transImg.shape[0] * transImg.shape[1]) ** 0.5)
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
    MIN_MATCH_COUNT = 10
    if len(good_pts) > MIN_MATCH_COUNT:
        trans_pts = np.float32([kp_trans[m.queryIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        orig_pts = np.float32([kp_orig[m.trainIdx].pt for m in good_pts]).reshape(-1, 1, 2)
        # 两种算法可选：cv2.LMEDS or cv2.RANSAC
        perArr, mask = cv2.findHomography(trans_pts / shrink_scale, orig_pts / shrink_scale, cv2.RANSAC, 5.0)
        return [np.array(perArr, dtype=np.float64)]
    else:
        print( "The images {} need {} points at least, but only match {} points." \
            .format(transImg_name, MIN_MATCH_COUNT, len(good_pts)))
        return None


def getBoundary(img, perArr):
    h, w = img.shape[0:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, perArr)
    maxVal = np.max(dst, axis=0)
    minVal = np.min(dst, axis=0)
    left_bound, right_bound = round(minVal[0][0]), round(maxVal[0][0])
    top_bound, bottom_bound = round(minVal[0][1]), round(maxVal[0][1])
    return int(left_bound), int(top_bound), int(right_bound), int(bottom_bound)


def PerArrs_Mutiply(perArrs, iters):
    if perArrs is not None:
        assert len(perArrs) >= iters
        arr = np.eye(3, dtype=np.float64)
        for i in range(iters):
            arr = np.dot(arr, perArrs[i])
        return arr


def getMaxBoundary(imgs, perArrs):
    min_left_bound = min_top_bound = 0
    max_right_bound = imgs[0].shape[1] - 1
    max_bottom_bound = imgs[0].shape[0] - 1

    for i in range(len(imgs)):
        arr = PerArrs_Mutiply(perArrs, i)
        left_bound, top_bound, right_bound, bottom_bound = getBoundary(imgs[i], arr)

        min_left_bound = min(min_left_bound, left_bound)
        min_top_bound = min(min_top_bound, top_bound)
        max_right_bound = max(max_right_bound, right_bound)
        max_bottom_bound = max(max_bottom_bound, bottom_bound)

    return min_left_bound, min_top_bound, max_right_bound, max_bottom_bound


def findMaxAreaContour(contours):  # 找出面积最大的封闭区域
    contours_area = [cv2.contourArea(contours[i]) for i in range(len(contours))]
    max_area_contour = contours[contours_area.index(max(contours_area))]
    return max_area_contour


@jit(nopython=True)
def calc_bound(mask):
    left = right = 0
    top = bottom = 0
    for col in range(0, mask.shape[1]):
        if mask[:, col].any():
            left = col
            break
    for col in range(mask.shape[1], 0, -1):
        if mask[:, col - 1].any():
            right = col
            break
    for row in range(0, mask.shape[0]):
        if mask[row, :].any():
            top = row
            break
    for row in range(mask.shape[0], 0, -1):
        if mask[row - 1, :].any():
            bottom = row
            break
    return left, right, top, bottom


# TODO: 将图像在mask扣取中出现的毛刺点消除（可能因为拼接图在黑色区域有压缩，导致非纯黑，使得mask存在毛刺点）
def getOverlayImgRegions(origImg, compImg, compImg_name, predict_img, predict_transArr):
    PerArrs = getTransformMatrix(predict_img, compImg, compImg_name)  # 获取变换矩阵

    if PerArrs is None:
        return None,None

    min_left_bound, min_top_bound, max_right_bound, max_bottom_bound \
        = getMaxBoundary([origImg, compImg], PerArrs)  # 获取最终拼接图像的最大边界
    new_width, new_height = (max_right_bound - min_left_bound + 1, max_bottom_bound - min_top_bound + 1)  # 计算拼接图像的宽和高

    # 考虑图像超出负边界时要进行正向平移，下面计算平移所对应的透视变换矩阵
    src_rect = np.float32([[min_left_bound, min_top_bound], [min_left_bound, max_bottom_bound],
                           [max_right_bound, max_bottom_bound], [max_right_bound, min_top_bound]]).reshape(-1, 1, 2)
    dst_rect = np.float32([[0, 0], [0, new_height - 1], [new_width - 1, new_height - 1],
                           [new_width - 1, 0]]).reshape(-1, 1, 2)
    transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)

    perArr = np.dot(transArr, PerArrs_Mutiply(PerArrs, 0))
    origWarpImg = cv2.warpPerspective(origImg, perArr, (new_width, new_height), flags=cv2.INTER_NEAREST)
    _, orig_mask = cv2.threshold(cv2.cvtColor(origWarpImg, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)

    if predict_transArr is not None:
        transArr = np.dot(transArr, np.linalg.inv(predict_transArr))
    perArr = np.dot(transArr, PerArrs_Mutiply(PerArrs, 1))
    compWarpImg = cv2.warpPerspective(compImg, perArr, (new_width, new_height), flags=cv2.cv2.INTER_NEAREST)
    _, comp_mask = cv2.threshold(cv2.cvtColor(compWarpImg, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)

    overlay_mask = cv2.bitwise_and(orig_mask, comp_mask)
    _, contours_overlay, _ = cv2.findContours(overlay_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    left, right, top, bottom = calc_bound(overlay_mask)
    overlay_origImg = origWarpImg[top:bottom + 1, left:right + 1]
    overlay_compImg = compWarpImg[top:bottom + 1, left:right + 1]
    overlay_mask = overlay_mask[top:bottom + 1, left:right + 1]

    overlay_origImg = cv2.bitwise_and(overlay_origImg, overlay_origImg, mask=overlay_mask)
    overlay_compImg = cv2.bitwise_and(overlay_compImg, overlay_compImg, mask=overlay_mask)

    # 把重叠区域映射回待比对图（由于无人机拍摄倾斜度的存在，用拼接图作为参考，重叠区域有一定变形）
    # ***** 若待比对图与拼接图只有部分区域重叠，则非重叠区域存在黑色区域 *****
    PerArrs = getTransformMatrix(compImg, overlay_compImg, compImg_name)
    if PerArrs is None:
        return None,None
    perArr = PerArrs_Mutiply(PerArrs, 1)
    h, w = compImg.shape[0:2]
    overlay_origImg = cv2.warpPerspective(overlay_origImg, perArr, (w, h), flags=cv2.cv2.INTER_NEAREST)
    overlay_compImg = cv2.warpPerspective(overlay_compImg, perArr, (w, h), flags=cv2.cv2.INTER_NEAREST)

    return [origWarpImg, overlay_origImg, overlay_compImg], contours_overlay


# 基于巴氏距离--cv2.HISTCMP_BHATTACHARYYA, similarity取值范围为[0,1]，值越小相似性越高，一般取阈值0.8
# 基于相关性--cv2.HISTCMP_CORREL, similarity取值范围为[-1,1]，绝对值越大相似性越高，一般取阈值0.2
def CalcHistSimilarity(img1, img2, mask=None):
    assert img1.shape == img2.shape, "计算直方图相似性的两张图片维度不一致"
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    # 只对色调和饱和度计算直方图，不考虑明度（忽略图像明暗的影响）
    h1 = cv2.calcHist([hsv1], [0, 1], mask, [90, 128], [0, 180, 0, 256])
    h1 = cv2.normalize(h1, h1, 0, 1, cv2.NORM_MINMAX, -1)
    h2 = cv2.calcHist([hsv2], [0, 1], mask, [90, 128], [0, 180, 0, 256])
    h2 = cv2.normalize(h2, h2, 0, 1, cv2.NORM_MINMAX, -1)
    similarity = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
    return abs(similarity)


def CalcHistSimilarity_withSplit(img1, img2, mask=None):
    assert img1.shape == img2.shape, "计算直方图相似性的两张图片维度不一致"
    block_size = 128
    row_num = int(img1.shape[0] / block_size) if img1.shape[0] > block_size else 1
    col_num = int(img1.shape[1] / block_size) if img1.shape[1] > block_size else 1
    img1 = cv2.resize(img1, (block_size * col_num, block_size * row_num), interpolation=cv2.INTER_AREA)
    img2 = cv2.resize(img2, (block_size * col_num, block_size * row_num), interpolation=cv2.INTER_AREA)
    mask = cv2.resize(mask, (block_size * col_num, block_size * row_num), interpolation=cv2.INTER_AREA) if (mask is not None) else None
    similarity = 0.0
    for i in range(row_num):
        for j in range(col_num):
            hsv1 = cv2.cvtColor(img1[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size], cv2.COLOR_BGR2HSV)
            hsv2 = cv2.cvtColor(img2[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size], cv2.COLOR_BGR2HSV)
            # 只对色调和饱和度计算直方图，不考虑明度（忽略图像明暗的影响）
            block_mask = mask[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size] if (mask is not None) else None
            h1 = cv2.calcHist([hsv1], [0, 1], block_mask, [90, 128], [0, 180, 0, 256])
            h1 = cv2.normalize(h1, h1, 0, 1, cv2.NORM_MINMAX, -1)
            h2 = cv2.calcHist([hsv2], [0, 1], block_mask, [90, 128], [0, 180, 0, 256])
            h2 = cv2.normalize(h2, h2, 0, 1, cv2.NORM_MINMAX, -1)
            block_similarity = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
            similarity += block_similarity
    return abs(similarity / (row_num * col_num))


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


# 压缩处理图像
def getShrinkImg(img, scale=1.0):
    if 0.0 < scale < 1.0:
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    else:
        return img


#############################################################################################################
# 基于结构性相似算法，对于无人机航摄图像提取差异目标效果不好，放弃使用。
def ImageCompare_SSIM(origImg, compImg, isShowImg=False):
    # 高斯滤波，要根据图像尺寸来动态选择合适大小的卷积核
    origImgBlur = cv2.GaussianBlur(origImg, (9, 9), 0)
    compImgBlur = cv2.GaussianBlur(compImg, (9, 9), 0)

    # 不调用结构性相似函数，直接相减求绝对值（缺点：1.没相似度评价值，2.效果不佳）
    # diff_img = cv2.absdiff(origImgBlur, compImgBlur)
    # diff_img = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
    # retval, img_binary = cv2.threshold(diff_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  #不需要黑白图反运算
    # print("computed threshold value: ", retval)

    (score, diff_img) = compare_ssim(origImgBlur, compImgBlur, multichannel=True, gaussian_weights=True, full=True)
    diff_img = (np.clip(diff_img, 0, 1) * 255).astype(np.uint8)
    diff_img = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
    retval, img_binary = cv2.threshold(diff_img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # 采用闭运算填充前景物体上的小黑点，可根据图像大小来适当增加闭运算迭代次数
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    img_binary = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    if isShowImg:
        print("SSIM = {}".format(score))
        print("computed threshold value: ", retval)
        Show_Img(diff_img, "Difference Image")
        Show_Img(img_binary, "Binary Image")

    _, contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    temp_area = compImg.shape[0] * compImg.shape[1]
    min_size_threshold = 0.0001 * temp_area  # 参数待调试
    max_size_threshold = 0.1 * temp_area  # 参数待调试
    similarity_threshold = 0.4  # 参数待调试
    possible_boxs = set()
    other_boxs = set()

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if min_size_threshold < w * h < max_size_threshold:
            # 计算直方图相似性时有必要采用掩模？
            # mask = None
            mask = cv2.fillPoly(np.zeros((h, w), np.uint8), [c - np.int32([x, y]).reshape(-1, 2)], 255)
            # similarity = CalcHistSimilarity(origImgBlur[y:y + h, x:x + w], compImgBlur[y:y + h, x:x + w], mask)
            similarity = CalcHistSimilarity_withSplit(origImgBlur[y:y + h, x:x + w], compImgBlur[y:y + h, x:x + w], mask)
            if similarity < similarity_threshold:
                possible_boxs.add((x, y, w, h))
            else:
                other_boxs.add((x, y, w, h))

    return possible_boxs, other_boxs


#############################################################################################################
# 基于选择性搜索算法来确定待比对图中目标
def selective_search(img, mode='single'):
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(img)
    # 各模式依次变慢，但提取目标候选质量提高，可根据需求选择
    if mode == 'single':
        ss.switchToSingleStrategy()
    elif mode == 'fast':
        ss.switchToSelectiveSearchFast()
    elif mode == 'quality':
        ss.switchToSelectiveSearchQuality()
    else:
        assert False, "mode must be \'single\' or \'fast\' or \'quality\'."
    return ss.process()


def excludeInvalidBoxs(boxs, min_size_threshold, max_size_threshold, long_size_threshold=9):
    selected_boxs = []
    for box in boxs:
        # excluding same rectangle (with different segments)
        if box in selected_boxs:
            continue
        x, y, w, h = box
        # excluding regions smaller than threshold
        if max_size_threshold <= w * h <= min_size_threshold:
            continue
        # excluding long rects
        if w / h >= long_size_threshold or h / w >= long_size_threshold:
            continue
        selected_boxs.append(box)
    return selected_boxs


# 计算两个重叠区域间的IoU和合并后的Box
def calcIoU(box1, box2):
    iou = 0.0
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    union_box = None
    intersect_w = min(x1 + w1, x2 + w2) - max(x1, x2)
    intersect_h = min(y1 + h1, y2 + h2) - max(y1, y2)

    if intersect_w > 0 and intersect_h > 0:
        intersect_area = intersect_w * intersect_h
        box1_area = w1 * h1
        box2_area = w2 * h2
        iou = intersect_area / float(box1_area + box2_area - intersect_area)
    if iou > 0:
        min_x = min(x1, x2)
        max_x = max(x1 + w1, x2 + w2)
        min_y = min(y1, y2)
        max_y = max(y1 + h1, y2 + h2)
        union_box = [min_x, min_y, max_x - min_x, max_y - min_y]
    return iou, union_box


def removeOverlayBoxs(boxs, iou_threshold=0.8):
    while True:
        temp_boxs = list(boxs)
        length = len(temp_boxs)
        for i in range(length - 1):
            if temp_boxs[i] not in boxs:
                continue
            for j in range(i + 1, length):
                if temp_boxs[j] not in boxs:
                    continue
                iou, union_box = calcIoU(temp_boxs[i], temp_boxs[j])
                if iou >= iou_threshold:
                    boxs.remove(temp_boxs[i])
                    if temp_boxs[j] in boxs:
                        boxs.remove(temp_boxs[j])
                    boxs.append(union_box)
                    break
        if len(boxs) == length:
            break
    return boxs


def getRestoredBoxs(boxs, scale=0.5):
    boxs = np.array(boxs, dtype=np.float32) / scale
    boxs = boxs.tolist()
    return boxs


def getSelectedBoxs(compImg):
    shrink_scale = 800.0 / ((compImg.shape[0] * compImg.shape[1]) ** 0.5)
    shrink_scale = 1.0 if shrink_scale > 1.0 else shrink_scale
    temp_compImg = getShrinkImg(compImg, scale=shrink_scale)

    selected_boxs = selective_search(temp_compImg, mode='single')

    temp_area = temp_compImg.shape[0] * temp_compImg.shape[1]
    min_size_threshold = 0.0001 * temp_area
    max_size_threshold = 0.01 * temp_area
    iou_threshold = 0.75
    selected_boxs = selected_boxs.tolist()
    selected_boxs = excludeInvalidBoxs(selected_boxs, min_size_threshold, max_size_threshold)
    selected_boxs = removeOverlayBoxs(selected_boxs, iou_threshold=iou_threshold)
    selected_boxs = getRestoredBoxs(selected_boxs, scale=shrink_scale)
    return selected_boxs


def ImageCompare_Hist(origImg, compImg, selected_boxs):
    origImgBlur = cv2.GaussianBlur(origImg, (9, 9), 0)
    compImgBlur = cv2.GaussianBlur(compImg, (9, 9), 0)

    similarity_threshold = 0.1  # 参数待调试
    possible_boxs = set()
    other_boxs = set()

    for box in selected_boxs:
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        similarity = CalcHistSimilarity(origImgBlur[y:y + h, x:x + w], compImgBlur[y:y + h, x:x + w])
        # similarity = CalcHistSimilarity_withSplit(origImgBlur[y:y + h, x:x + w], compImgBlur[y:y + h, x:x + w])
        if similarity < similarity_threshold:
            possible_boxs.add((x, y, w, h))
        else:
            other_boxs.add((x, y, w, h))

    return possible_boxs, other_boxs


def ImageCompare_Deep(origImg, compImg, selected_boxs, similarity):
    # TODO: 传递目标候选框便于使用图像生成器，避免直接传递大量的图像列表，使得内存开销较大
    distances = similarity.compare_images(origImg, compImg, selected_boxs)
    possible_boxs = set()
    other_boxs = set()
    similarity_threshold = 0.6
    for i in range(len(distances)):
        box = selected_boxs[i]
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        if distances[i] < similarity_threshold:
            possible_boxs.add((x, y, w, h))
        else:
            other_boxs.add((x, y, w, h))
    return possible_boxs, other_boxs


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


def convert_gps(coord_arr):
    arr = str(coord_arr).replace('[', '').replace(']', '').replace('\'', '').split(', ')
    d = float(arr[0].split('/')[0]) / float(arr[0].split('/')[1])
    m = float(arr[1].split('/')[0]) / float(arr[1].split('/')[1])
    s = float(arr[2].split('/')[0]) / float(arr[2].split('/')[1])
    return float(d) + (float(m) / 60) + (float(s) / 3600)


def get_gps(file):
    try:
        exif_dict = pyexiv2.Image(file, encoding='gbk').read_exif()
        long = exif_dict.get("Exif.GPSInfo.GPSLongitude").split()
        long = convert_gps(long)
        lat = exif_dict.get("Exif.GPSInfo.GPSLatitude").split()
        lat = convert_gps(lat)
        alt = exif_dict.get("Exif.GPSInfo.GPSAltitude")
        alt = float(alt.split('/')[0]) / float(alt.split('/')[1])
    except Exception as e:
        print("Exception:", e)
        print("请确保图像文件" + file + "包含经纬度等EXIF有效信息！")
        return None
    else:
        return [long, lat, alt]


"""
########################################################
# 测试使用Geodesic.WGS84来使用经纬度转地面实际距离
if __name__ == '__main__':
    suffix = ".JPG"
    origImgs_path = "./imgs/input_images/"
    origImg_files, origImg_names = getImgList(origImgs_path, suffix, reverse=False)
    gps_list = {}
    for i, f in enumerate(origImg_files):
        gps_info = get_gps(f)
        print(origImg_names[i] + " GPS_info: " + "long=" + str(gps_info[0]) + " lat=" + str(gps_info[1]) + " alt=" + str(gps_info[2]))
        gps_list.update({origImg_names[i]: gps_info})

    compImg_file = "./imgs/DJI_0028.JPG"
    gps_info = get_gps(compImg_file)
    min_distance = float('inf')
    selected_file = ""
    for key in gps_list.keys():
        geo_distance = Geodesic.WGS84.Inverse(gps_info[1], gps_info[0], gps_list[key][1], gps_list[key][0]).get("s12")
        if min_distance > geo_distance:
            min_distance = geo_distance
            selected_file = key
    print("min_distance =", min_distance)
    print("selected_file:", selected_file)
########################################################
"""

if __name__ == '__main__':
    start_time = time.time()
    origImg = cv2.imread("./imgs/merged_img.JPG")
    compFile = "./imgs/DJI_0009.JPG"
    compImg = get_square_img(cv2.imread(compFile))
    compImg_gps = get_gps(compFile)

    with open("./imgs/gps_points.csv", mode='r') as file_handle:
        csv_rows = csv.reader(file_handle)
        arr_gps = np.array([row for index, row in enumerate(csv_rows) if index > 0], dtype=np.float64)

    '''
    from sklearn.linear_model import LinearRegression
    # 用线性回归预测新输入GPS坐标所对应的图像坐标（误差较大）
    gps_model_x = LinearRegression()
    gps_model_x.fit(arr_gps[:, 2].reshape(-1, 1), arr_gps[:, 0].reshape(-1, 1))
    gps_model_y = LinearRegression()
    gps_model_y.fit(arr_gps[:, 3].reshape(-1, 1), arr_gps[:, 1].reshape(-1, 1))
    img = np.copy(origImg)
    #init_x = gps_model_x.predict(np.array([compImg_gps[0]]).reshape(-1, 1))
    #init_y = gps_model_y.predict(np.array([compImg_gps[1]]).reshape(-1, 1))
    #img = cv2.circle(img, (init_x, init_y), 100, (0, 0, 255), -1)

    points_x = gps_model_x.predict(arr_gps[:, 2].reshape(-1, 1))
    points_y = gps_model_y.predict(arr_gps[:, 3].reshape(-1, 1))
    for i in range(len(arr_gps)):
        img = cv2.circle(img, (int(arr_gps[i, 0]), int(arr_gps[i, 1])), 100, (0, 0, 255), -1)
        img = cv2.circle(img, (int(points_x[i, 0]), int(points_y[i, 0])), 80, (255, 0, 0), -1)
    Show_Img(img, "img", lastFlag=True)
    '''
    x_predict_func = interpolate.interp1d(arr_gps[:, 2], arr_gps[:, 0], kind="slinear")
    y_predict_func = interpolate.interp1d(arr_gps[:, 3], arr_gps[:, 1], kind="slinear")

    try:
        predict_x = int(x_predict_func(np.array([compImg_gps[0]])))
        predict_y = int(y_predict_func(np.array([compImg_gps[1]])))
    except ValueError as e:
        print("Exception:", e)
        print("不能通过GPS信息插值进行位置预测, 取距离最近点作为预测点。")
        min_distance = float('inf')
        predict_x = None
        predict_y = None
        for item in arr_gps:
            geo_distance = Geodesic.WGS84.Inverse(compImg_gps[1], compImg_gps[0], item[3], item[2]).get("s12")
            if min_distance > geo_distance:
                min_distance = geo_distance
                predict_x, predict_y = (int(item[0]), int(item[1]))

    h, w, _ = compImg.shape
    predict_img = np.zeros_like(origImg)
    cv2.rectangle(predict_img, (predict_x - int(w / 2), predict_y - int(h / 2)),
                  (predict_x + int(w / 2), predict_y + int(h / 2)), (255, 255, 255), -1)
    predict_img = cv2.bitwise_and(origImg, predict_img)

    _, mask = cv2.threshold(cv2.cvtColor(predict_img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
    left, right, top, bottom = calc_bound(mask)
    predict_img = predict_img[top:bottom + 1, left:right + 1]

    h, w, _ = predict_img.shape
    src_rect = np.float32([[left, top], [left, bottom], [right, bottom], [right, top]]).reshape(-1, 1, 2)
    dst_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    predict_transArr = cv2.getPerspectiveTransform(src_rect, dst_rect).astype(np.float64)

    img_list, contours = getOverlayImgRegions(getShrinkImg(origImg, scale=1.0), getShrinkImg(compImg, scale=1.0),
                                              os.path.basename(compFile), getShrinkImg(predict_img, scale=1.0), predict_transArr)

    ImgPosition, origImgRegion, compImgRegion = tuple(img_list)
    cv2.drawContours(ImgPosition, contours, -1, (0, 0, 255), 10)
    (x, y, w, h) = cv2.boundingRect(findMaxAreaContour(contours))
    cv2.putText(ImgPosition, "Searched from " + os.path.basename(compFile), (x + int(w / 4), y + int(h / 2)),
                cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 3)

    similarity = ism.ImageSimilarity()
    similarity.batch_size = 32
    
    selected_boxs = getSelectedBoxs(compImgRegion)
    # possible_boxs, other_box = ImageCompare_Hist(origImgRegion, compImgRegion, selected_boxs)
    possible_boxs, other_box = ImageCompare_Deep(origImgRegion, compImgRegion, selected_boxs, similarity)
    for (x, y, w, h) in possible_boxs:
        cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
        cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 128, 255), 5)
    '''
    for (x, y, w, h) in other_box:
        cv2.rectangle(origImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.rectangle(compImgRegion, (x, y), (x + w, y + h), (0, 255, 0), 5)
    '''
    Show_Img(ImgPosition, "ImgPosition")
    Show_Img(origImgRegion, "origImgRegion")
    Show_Img(compImgRegion, "compImgRegion", lastFlag=True)
    total_time = time.time() - start_time
    print('total cost time:', total_time)
