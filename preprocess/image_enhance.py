import cv2
import numpy as np
from numba import jit


# 自适应Gamma校正（图像偏亮或偏暗时可用）
def gamma_trans(img, gamma=0.5):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    gamma = np.log(gamma) / np.log(img.mean() / 255.0)  # gamma值根据原始图像的平均亮度进行选取
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # apply gamma correction using the lookup table
    return cv2.LUT(img, gamma_table)


# 直方图均衡化（增强）
def hist_equal(img):
    b, g, r = cv2.split(img)
    dest_b = cv2.equalizeHist(b)
    dest_g = cv2.equalizeHist(g)
    dest_r = cv2.equalizeHist(r)
    dest = cv2.merge([dest_b, dest_g, dest_r])
    return dest


# 对比度受限的自适应直方图均衡化（CLAHE）
def hist_equal_CLAHE(img, clipLimit=1.0, tileGridSize=(9, 9)):
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    b, g, r = cv2.split(img)
    dest_b = clahe.apply(b)
    dest_g = clahe.apply(g)
    dest_r = clahe.apply(r)
    dest = cv2.merge([dest_b, dest_g, dest_r])
    return dest


# 基于拉普拉斯变换的图像锐化
def img_sharpen(img):
    gauss = cv2.GaussianBlur(img, (3, 3), 0)
    lap = cv2.Laplacian(gauss, cv2.CV_16S)
    lap = cv2.convertScaleAbs(lap)
    dest = cv2.add(img, lap)  # 直接相加貌似不合适?
    return dest


#######################处理速度太慢#############################
# 将灰度数组映射为直方图字典，nums表示灰度的数量级
def arrayToHist(grayArray, nums):
    if (len(grayArray.shape) != 2):
        print("length error")
        return None

    w, h = grayArray.shape
    hist = {}
    for k in range(nums):
        hist[k] = 0
    for i in range(w):
        for j in range(h):
            if (hist.get(grayArray[i][j]) is None):
                hist[grayArray[i][j]] = 0
            hist[grayArray[i][j]] += 1

    # normalize
    n = w * h
    for key in hist.keys():
        hist[key] = float(hist[key]) / n
    return hist


def hist_match_for_gray(src_img, tmp_img):
    # 计算累计直方图
    src_hist = arrayToHist(src_img, 256)
    tmp = 0.0
    hs_acc = src_hist.copy()
    for i in range(256):
        tmp += src_hist[i]
        hs_acc[i] = tmp

    tmp_hist = arrayToHist(tmp_img, 256)
    tmp = 0.0
    ht_acc = tmp_hist.copy()
    for i in range(256):
        tmp += tmp_hist[i]
        ht_acc[i] = tmp

    # 计算映射
    M = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        idx = 0
        minv = 1
        for j in range(256):
            if (np.fabs(ht_acc[j] - hs_acc[i]) < minv):
                minv = np.fabs(ht_acc[j] - hs_acc[i])
                idx = j
        M[i] = idx
    res = M[src_img]
    return res


def hist_match_for_rgb(src_img, tmp_img):
    src_b, src_g, src_r = cv2.split(src_img)
    tmp_b, tmp_g, tmp_r = cv2.split(tmp_img)
    dest_b = hist_match_for_gray(src_b, tmp_b)
    dest_g = hist_match_for_gray(src_g, tmp_g)
    dest_r = hist_match_for_gray(src_r, tmp_r)
    dest = cv2.merge([dest_b, dest_g, dest_r])
    return dest


##################################################################

# 直方图规定化（直方图匹配）
def hist_match_new(src_img, tmp_img):
    color = ('r', 'g', 'b')
    h, w, _ = src_img.shape
    src_pts = src_img.shape[0] * src_img.shape[1]
    tmp_pts = tmp_img.shape[0] * tmp_img.shape[1]
    res_img = src_img.copy()

    for i in range(len(color)):
        src_hist = cv2.calcHist([src_img], [i], None, [256], [0, 256])
        tmp_hist = cv2.calcHist([tmp_img], [i], None, [256], [0, 256])
        src_cdf_hist = src_hist.cumsum() / src_pts  # 灰度值的累计值的比率
        tmp_cdf_hist = tmp_hist.cumsum() / tmp_pts

        diff_cdf = np.zeros((256, 256), dtype=np.float32)  # diff_cdf存储每2个灰度值比率间的差值
        '''
        for j in range(256):
            for k in range(256):
                diff_cdf[j][k] = abs(src_cdf_hist[j] - tmp_cdf_hist[k])
        '''
        diff_cdf = np.fabs(np.tile(src_cdf_hist, (256, 1)).T - np.tile(tmp_cdf_hist, (256, 1)))

        LUT = np.zeros(256, dtype=np.uint8)  # 映射表
        for j in range(256):
            min_val = diff_cdf[j, 0]
            index = 0
            for k in range(256):  # 直方图规定化的映射原理
                if min_val > diff_cdf[j, k]:
                    min_val = diff_cdf[j, k]
                    index = k
            LUT[j] = index

        res_img[:, :, i] = LUT[res_img[:, :, i]]  # 对原图像进行单个通道值的映射
    return res_img


#######################################################
# 貌似有问题，增强后图像是灰色的
def replaceZeroes(data):
    min_nonzero = min(data[np.nonzero(data)])
    data[data == 0] = min_nonzero
    return data


def simple_color_balance(input_img, s1, s2):
    h, w = input_img.shape[:2]
    temp_img = input_img.copy()
    one_dim_array = temp_img.flatten()
    sort_array = sorted(one_dim_array)

    per1 = int((h * w) * s1 / 100)
    minvalue = sort_array[per1]

    per2 = int((h * w) * s2 / 100)
    maxvalue = sort_array[(h * w) - 1 - per2]

    # 实施简单白平衡算法
    if (maxvalue <= minvalue):
        out_img = np.full(input_img.shape, maxvalue)
    else:
        scale = 255.0 / (maxvalue - minvalue)
        out_img = np.where(temp_img < minvalue, 0, temp_img)  # 防止像素溢出
        out_img = np.where(out_img > maxvalue, 255, out_img)  # 防止像素溢出
        out_img = scale * (out_img - minvalue)  # 映射中间段的图像像素
        out_img = cv2.convertScaleAbs(out_img)
    return out_img


def SSR(src_img, size):
    L_blur = cv2.GaussianBlur(src_img, (size, size), 0)
    img = replaceZeroes(src_img)
    L_blur = replaceZeroes(L_blur)

    dst_Img = np.log(img / 255.0)
    dst_Lblur = np.log(L_blur / 255.0)
    log_R = np.subtract(dst_Img, dst_Lblur)
    dst_R = np.exp(log_R) * 255
    dst_R = cv2.normalize(dst_R, None, 0, 255, cv2.NORM_MINMAX)
    log_uint8 = cv2.convertScaleAbs(dst_R)
    log_uint8 = simple_color_balance(log_uint8, 2, 3)
    return log_uint8


######################################################

if __name__ == '__main__':
    src = cv2.imread("./img/canon.bmp")
    # src = cv2.resize(src, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    # 高斯滤波去噪
    # dest = cv2.GaussianBlur(src,(3,3),0)

    # 双边滤波去噪
    # dest = cv2.bilateralFilter(src,3,75,75)

    # 非局部平均值去噪
    # dest = cv2.fastNlMeansDenoisingColored(src,None,3,3,5,9)

    # dest = gamma_trans(src)
    # dest = hist_equal(src)
    # dest = hist_equal_CLAHE(src)
    # dest = img_sharpen(src)
    dest = SSR(src, 9)

    # tmp = cv2.imread("./img/DJI_0008.JPG")
    # dest = hist_match_for_rgb(src, tmp)
    # cv2.imwrite('./img/Test-HM.JPG',dest)
    contrast = np.hstack((src, dest))
    cv2.imshow("contrast", contrast)
