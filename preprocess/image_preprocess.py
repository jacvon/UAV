import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageStat
import matplotlib.pyplot as plt
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


#######################################################
# 直方图规定化（或直方图匹配）
def hist_match(src_img, tmp_img):
    color = ('r', 'g', 'b')
    h, w, _ = src_img.shape
    src_pts = src_img.shape[0] * src_img.shape[1]
    tmp_pts = tmp_img.shape[0] * tmp_img.shape[1]
    res_img = src_img.copy()

    @jit(nopython=True)
    def calcLUT(diff_cdf):
        LUT = np.zeros(256, dtype=np.uint8)  # 映射表
        for j in range(256):
            min_val = diff_cdf[j, 0]
            index = 0
            for k in range(256):  # 直方图规定化的映射原理
                if min_val > diff_cdf[j, k]:
                    min_val = diff_cdf[j, k]
                    index = k
            LUT[j] = index
        return LUT

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
        res_img[:, :, i] = calcLUT(diff_cdf)[res_img[:, :, i]]  # 对原图像进行单个通道值的映射
    return res_img


#######################################################


#######################################################
# 三种Retinex图像增强算法：可用于去雾（但对于大图运算较慢）

# 色彩平衡: 将1%的最大值和最小值设置为255和0，其余值映射为(0,255)
#@jit(nopython=True)
def color_balance(img, low_clip=0.01, high_clip=0.99):
    size = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / size < low_clip:
                low_val = u
            if float(current) / size > high_clip:
                high_val = u
            current += c
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img


# 单尺度Retinex算法: sigma=300
def single_scale_retinex(img, sigma=300):
    gaussian = cv2.GaussianBlur(img, (0, 0), sigma)

    log_img = np.log(img / 255.0 + 0.001)
    log_gaussian = np.log(gaussian / 255.0 + 0.001)
    sub_img = np.subtract(log_img, log_gaussian)
    exp_img = np.exp(sub_img)

    dst_img = cv2.normalize(exp_img, None, 0, 255, cv2.NORM_MINMAX)
    dst_img = cv2.convertScaleAbs(dst_img)
    dst_img = color_balance(dst_img)
    return dst_img


# 多尺度Retinex算法
def multi_scale_retinex(img, sigma_list=[10, 50, 250]):
    log_img = np.log(img / 255.0 + 0.001)

    def get_single_sub_retinex(img, log_img, sigma):
        gaussian = cv2.GaussianBlur(img, (0, 0), sigma)
        log_gaussian = np.log(gaussian / 255.0 + 0.001)
        sub_retinex = np.subtract(log_img, log_gaussian)
        return sub_retinex

    sum_retinex = np.zeros_like(img, dtype=np.float32)
    for sigma in sigma_list:
        sum_retinex += get_single_sub_retinex(img, log_img, sigma)
    exp_img = np.exp(sum_retinex / len(sigma_list))
    dst_img = cv2.normalize(exp_img, None, 0, 255, cv2.NORM_MINMAX)
    dst_img = cv2.convertScaleAbs(dst_img)
    dst_img = color_balance(dst_img)
    return dst_img


# 具有色彩恢复的多尺度Retinex算法(Multi-Scale Retinex with Color-Restoration)
def MSRCR(img, sigma_list=[10, 50, 250], gain=5, offset=25, alpha=125, beta=46):
    img = np.float64(img)

    def get_single_sub_retinex(img, log_img, sigma):
        gaussian = cv2.GaussianBlur(img, (0, 0), sigma)
        log_gaussian = np.log(gaussian / 255.0 + 0.001)
        sub_retinex = np.subtract(log_img, log_gaussian)
        return sub_retinex

    def get_multi_sub_retinex(img, sigma_list):
        log_img = np.log(img / 255.0 + 0.001)
        sub_retinex = np.zeros_like(img, dtype=np.float32)
        for sigma in sigma_list:
            sub_retinex += get_single_sub_retinex(img, log_img, sigma)
        sub_retinex = sub_retinex / len(sigma_list)
        return sub_retinex

    def color_restoration(img, alpha, beta):
        img_sum = np.sum(img, axis=2, keepdims=True)
        color = beta * (np.log10(alpha * img + 1.0) - np.log10(img_sum + 1.0))
        return color

    sub_retinex = get_multi_sub_retinex(img, sigma_list)
    exp_img = np.exp(sub_retinex)
    cr = color_restoration(img, alpha, beta)
    dst_img = gain * (exp_img * cr + offset)
    dst_img = cv2.normalize(dst_img, None, 0, 255, cv2.NORM_MINMAX)
    dst_img = cv2.convertScaleAbs(dst_img)
    dst_img = color_balance(dst_img)
    return dst_img


######################################################


######################################################
# 图像亮度均衡化
# 获取亮度值
def get_brightness_from_path(path):
    img = Image.open(path)
    stat = ImageStat.Stat(img)
    # r, g, b = stat.mean  # 基于像素平均与经验公式
    r, g, b = stat.rms  # 基于像素均方根与经验公式
    brightness = (0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2)) ** 0.5
    return brightness


# 获取亮度值
def get_brightness_from_img(pil_img):
    stat = ImageStat.Stat(pil_img)
    # r, g, b = stat.mean  # 基于像素平均与经验公式
    r, g, b = stat.rms  # 基于像素均方根与经验公式
    brightness = (0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2)) ** 0.5
    return brightness


# 获取亮度平均值
def get_avg_brightness(img_paths):
    brightness_sum = 0.0
    for path in img_paths:
        brightness = get_brightness_from_path(path)
        brightness_sum += brightness
    avg = brightness_sum / len(img_paths)
    return avg


# 设置图像亮度
def set_brightness(img_pil, ref_brightness):
    cur_brightness = get_brightness_from_img(img_pil)
    img = ImageEnhance.Brightness(img_pil).enhance(ref_brightness / cur_brightness)
    return img


# 批量均衡图像亮度
def uniform_brightness(img_paths):
    avg_brightness = get_avg_brightness(img_paths)
    for path in img_paths:
        img = Image.open(path)
        cur_brightness = get_brightness_from_img(img)
        img = ImageEnhance.Brightness(img).enhance(avg_brightness / cur_brightness)
    return img


######################################################


######################################################
# 图像白平衡处理
def WhiteBlance(img, mode=1):
    """白平衡处理（默认为1均值、2灰度世界、3基于图像分析的偏色检测及颜色校正、4动态阈值）"""
    # 读取图像
    b, g, r = cv2.split(img)
    # 均值变为三通道
    h, w, _ = img.shape
    if mode == 2:
        # 灰度世界假设
        b_avg, g_avg, r_avg = cv2.mean(b)[0], cv2.mean(g)[0], cv2.mean(r)[0]
        # 需要调整的RGB分量的增益
        k = (b_avg + g_avg + r_avg) / 3
        kb, kg, kr = k / b_avg, k / g_avg, k / r_avg
        ba, ga, ra = b * kb, g * kg, r * kr

        output_img = cv2.merge([ba, ga, ra])
    elif mode == 3:
        # 基于图像分析的偏色检测及颜色校正
        I_b_2, I_r_2 = np.double(b) ** 2, np.double(r) ** 2
        sum_I_b_2, sum_I_r_2 = np.sum(I_b_2), np.sum(I_r_2)
        sum_I_b, sum_I_g, sum_I_r = np.sum(b), np.sum(g), np.sum(r)
        max_I_b, max_I_g, max_I_r = np.max(b), np.max(g), np.max(r)
        max_I_b_2, max_I_r_2 = np.max(I_b_2), np.max(I_r_2)
        [u_b, v_b] = np.matmul(np.linalg.inv([[sum_I_b_2, sum_I_b], [max_I_b_2, max_I_b]]), [sum_I_g, max_I_g])
        [u_r, v_r] = np.matmul(np.linalg.inv([[sum_I_r_2, sum_I_r], [max_I_r_2, max_I_r]]), [sum_I_g, max_I_g])
        b0 = np.uint8(u_b * (np.double(b) ** 2) + v_b * b)
        r0 = np.uint8(u_r * (np.double(r) ** 2) + v_r * r)
        output_img = cv2.merge([b0, g, r0])
    elif mode == 4:
        # 动态阈值算法 ---- 白点检测和白点调整
        # 只是白点检测不是与完美反射算法相同的认为最亮的点为白点，而是通过另外的规则确定
        def con_num(x):
            if x > 0:
                return 1
            if x < 0:
                return -1
            if x == 0:
                return 0

        yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        # YUV空间
        (y, u, v) = cv2.split(yuv_img)
        max_y = np.max(y.flatten())
        sum_u, sum_v = np.sum(u), np.sum(v)
        avl_u, avl_v = sum_u / (h * w), sum_v / (h * w)
        du, dv = np.sum(np.abs(u - avl_u)), np.sum(np.abs(v - avl_v))
        avl_du, avl_dv = du / (h * w), dv / (h * w)
        radio = 0.5  # 如果该值过大过小，色温向两极端发展

        valuekey = np.where((np.abs(u - (avl_u + avl_du * con_num(avl_u))) < radio * avl_du)
                            | (np.abs(v - (avl_v + avl_dv * con_num(avl_v))) < radio * avl_dv))
        num_y, yhistogram = np.zeros((h, w)), np.zeros(256)
        num_y[valuekey] = np.uint8(y[valuekey])
        yhistogram = np.bincount(np.uint8(num_y[valuekey].flatten()), minlength=256)
        ysum = len(valuekey[0])
        Y = 255
        num, key = 0, 0
        while Y >= 0:
            num += yhistogram[Y]
            if num > 0.1 * ysum:  # 取前10%的亮点为计算值，如果该值过大易过曝光，该值过小调整幅度小
                key = Y
                break
            Y = Y - 1

        sumkey = np.where(num_y > key)
        sum_b, sum_g, sum_r = np.sum(b[sumkey]), np.sum(g[sumkey]), np.sum(r[sumkey])
        num_rgb = len(sumkey[0])

        b0 = np.double(b) * int(max_y) / (sum_b / num_rgb)
        g0 = np.double(g) * int(max_y) / (sum_g / num_rgb)
        r0 = np.double(r) * int(max_y) / (sum_r / num_rgb)

        output_img = cv2.merge([b0, g0, r0])
    else:
        # 默认均值  ---- 简单的求均值白平衡法
        b_avg, g_avg, r_avg = cv2.mean(b)[0], cv2.mean(g)[0], cv2.mean(r)[0]
        # 求各个通道所占增益
        k = (b_avg + g_avg + r_avg) / 3
        kb, kg, kr = k / b_avg, k / g_avg, k / r_avg
        b = cv2.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)
        g = cv2.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
        r = cv2.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
        output_img = cv2.merge([b, g, r])
    output_img = np.uint8(np.clip(output_img, 0, 255))
    return output_img


######################################################


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


if __name__ == '__main__':
    src = cv2.imread("./img/DJI_0008.JPG")
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


    # dest = single_scale_retinex(src)
    # dest = multi_scale_retinex(src)
    # dest = MSRCR(src)

    # dest = WhiteBlance(src, mode=1)

    templete = cv2.imread("./img/DJI_0012.JPG")
    dest = hist_match(src, templete)
    # cv2.imwrite('./img/test_hist_match.JPG',dest)

    contrast = np.hstack((src, dest))
    Show_Img(contrast, title="contrast", lastFlag=True)
