import cv2
import numpy as np


def DarkChannel(im, sz):
    b, g, r = cv2.split(im)
    dc = cv2.min(cv2.min(r, g), b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
    dark = cv2.erode(dc, kernel)
    # cv2.imshow("dark img", dark)
    return dark


def AtmLight(im, dark):
    [h, w] = im.shape[:2]
    imsz = h * w
    numpx = max(int(imsz / 1000.0), 10)
    darkvec = dark.reshape(imsz)
    imvec = im.reshape(imsz, 3)
    indices = darkvec.argsort()
    indices = indices[imsz - numpx::]

    # atmsum = np.zeros(3)
    # for ind in range(0,numpx):
    #   atmsum = atmsum + imvec[indices[ind],:]
    # airlight = atmsum/numpx
    airlight = np.mean(imvec[indices, :], axis=0)
    return airlight


def AirlightEstimation(img):
    global airlight
    [h, w] = img.shape[:2]

    if h * w > 256:
        lu_img = img[0:round(h / 2.0), 0:round(w / 2.0), :]
        ru_img = img[round(h / 2.0):h, 0:round(w / 2.0), :]
        lb_img = img[0:round(h / 2.0), round(w / 2.0):w, :]
        rb_img = img[round(h / 2.0):h, round(w / 2.0):w, :]

        lu_mean = np.zeros(3)
        ru_mean = np.zeros(3)
        lb_mean = np.zeros(3)
        rb_mean = np.zeros(3)

        lu_std = np.zeros(3)
        ru_std = np.zeros(3)
        lb_std = np.zeros(3)
        rb_std = np.zeros(3)

        for i in range(3):
            lu_mean[i] = np.mean(lu_img[:, :, i])
            ru_mean[i] = np.mean(ru_img[:, :, i])
            lb_mean[i] = np.mean(lb_img[:, :, i])
            rb_mean[i] = np.mean(rb_img[:, :, i])

            lu_std[i] = np.std(lu_img[:, :, i])
            ru_std[i] = np.std(ru_img[:, :, i])
            lb_std[i] = np.std(lb_img[:, :, i])
            rb_std[i] = np.std(rb_img[:, :, i])

        assert ((lu_mean - lu_std).all() > 0)
        assert ((ru_mean - ru_std).all() > 0)
        assert ((lb_mean - lb_std).all() > 0)
        assert ((rb_mean - rb_std).all() > 0)
        lu_score = np.sum(lu_mean - lu_std)
        ru_score = np.sum(ru_mean - ru_std)
        lb_score = np.sum(lb_mean - lb_std)
        rb_score = np.sum(rb_mean - rb_std)

        x = [lu_score, ru_score, lb_score, rb_score]
        if max(x) == lu_score:
            AirlightEstimation(lu_img)
        elif max(x) == ru_score:
            AirlightEstimation(ru_img)
        elif max(x) == lb_score:
            AirlightEstimation(lb_img)
        else:
            AirlightEstimation(rb_img)
    else:
        # 全局大气光校正
        dc = DarkChannel(img, 3)
        bright_pixel = dc[0, 0]
        bright_index = (0, 0)
        dark_pixel = dc[0, 0]
        dark_index = (0, 0)
        bright_count = 0
        dark_count = 0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_gray = np.mean(gray)

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                if gray[i, j] >= mean_gray:
                    bright_count += 1
                    if bright_pixel < dc[i, j]:
                        bright_pixel = dc[i, j]
                        bright_index = (i, j)
                if gray[i, j] < mean_gray:
                    dark_count += 1
                    if dark_pixel < dc[i, j]:
                        dark_pixel = dc[i, j]
                        dark_index = (i, j)
        total_count = float(gray.shape[0] * gray.shape[1])
        airlight = bright_count / total_count * img[bright_index[0], bright_index[1], :] \
                   + dark_count / total_count * img[dark_index[0], dark_index[1], :]
        '''
        distance=np.square(1-img[:,:,0])+np.square(1-img[:,:,1])+np.square(1-img[:,:,2])
        #pos=np.where(distance==np.maximum(distance))  #貌似计算开销更大...
        pos=np.unravel_index(np.argmin(distance),distance.shape)
        airlight=img[pos[0],pos[1],:]
        '''
    return airlight


def TransmissionEstimate(im, A, sz):
    omega = 0.95
    # temp = np.empty(im.shape,im.dtype)
    # for ind in range(0,3):
    #    temp[:,:,ind] = im[:,:,ind]/A[ind]
    temp = im / A
    te = 1 - omega * DarkChannel(temp, sz)
    return te


def TransmissionEstimateNew(img, A, sz):
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(sz,sz))
    b_min,g_min,r_min = cv2.split((A-img)/A)
    dc_min = cv2.min(cv2.min(r_min,g_min),b_min)
    t_min = cv2.erode(dc_min,kernel)
    t_min=np.float32(t_min)

    b_max,g_max,r_max = cv2.split((img-A)/(1-A))
    dc_max = cv2.max(cv2.max(r_max,g_max),b_max)
    t_max = cv2.dilate(dc_max,kernel)
    t_max=np.float32(t_max)
    te=cv2.max(t_min,t_max)
    return te
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
    img_min = cv2.erode((A - img) / A, kernel)
    b_min, g_min, r_min = cv2.split(img_min)
    dc_min = cv2.min(cv2.min(r_min, g_min), b_min)

    img_max = cv2.dilate((img - A) / (1 - A), kernel)
    b_max, g_max, r_max = cv2.split(img_max)
    dc_max = cv2.max(cv2.max(r_max, g_max), b_max)
    te = cv2.max(dc_min, dc_max)
    return te


def Guidedfilter(guide, src, r, eps):  # 引导滤波（可直接调用cv2内置函数）
    return cv2.ximgproc.guidedFilter(guide, src, r, eps)
    '''
    mean_I = cv2.boxFilter(guide,cv2.CV_32F,(r,r))
    mean_p = cv2.boxFilter(src, cv2.CV_32F,(r,r))
    mean_Ip = cv2.boxFilter(guide*src,cv2.CV_32F,(r,r))
    cov_Ip = mean_Ip - mean_I*mean_p
    mean_II = cv2.boxFilter(guide*guide,cv2.CV_32F,(r,r))
    var_I   = mean_II - mean_I*mean_I
    a = cov_Ip/(var_I + eps)
    b = mean_p - a*mean_I
    mean_a = cv2.boxFilter(a,cv2.CV_32F,(r,r))
    mean_b = cv2.boxFilter(b,cv2.CV_32F,(r,r))
    res = mean_a*guide + mean_b
    return res
    '''


def fastGuidedfilter(guide, src, r, eps, k=4):  # 快速引导滤波
    scale = 1.0 / k
    guide_ = cv2.resize(guide, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    src_ = cv2.resize(src, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    r_ = round(r * scale)
    mean_I = cv2.boxFilter(guide_, cv2.CV_32F, (r_, r_))
    mean_p = cv2.boxFilter(src_, cv2.CV_32F, (r_, r_))
    mean_Ip = cv2.boxFilter(guide_ * src_, cv2.CV_32F, (r_, r_))
    cov_Ip = mean_Ip - mean_I * mean_p
    mean_II = cv2.boxFilter(guide_ * guide_, cv2.CV_32F, (r_, r_))
    var_I = mean_II - mean_I * mean_I
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I
    mean_a = cv2.boxFilter(a, cv2.CV_32F, (r_, r_))
    mean_b = cv2.boxFilter(b, cv2.CV_32F, (r_, r_))
    mean_A = cv2.resize(mean_a, (guide.shape[1], guide.shape[0]), interpolation=cv2.INTER_AREA)
    mean_B = cv2.resize(mean_b, (guide.shape[1], guide.shape[0]), interpolation=cv2.INTER_AREA)
    res = mean_A * guide + mean_B
    return res


def TransmissionRefine(im, te):
    r = 101
    eps = 0.001
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    tr = Guidedfilter(gray, te, r, eps)
    # cv2.imshow("transmission img", tr)
    return tr


# 自适应Gamma校正（图像偏亮或偏暗时可用）
def gamma_trans(img, gamma=0.5):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    gamma = np.log(gamma) / np.log(img.mean() / 255.0)  # gamma值根据原始图像的平均亮度进行选取
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # apply gamma correction using the lookup table
    return cv2.LUT(img, gamma_table)


# 自适应Gamma校正（图像偏亮或偏暗时可用）
def gamma_trans(img, gamma=0.5):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    gamma = np.log(gamma) / np.log(img.mean() / 255.0)  # gamma值根据原始图像的平均亮度进行选取
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # apply gamma correction using the lookup table
    return cv2.LUT(img, gamma_table)


def RestoreImg(im, t, A):
    tx = 0.1
    t = cv2.max(t, tx)
    # res = np.empty(im.shape,im.dtype)
    # for ind in range(0,3):
    #    res[:,:,ind] = (im[:,:,ind]-A[ind])/t + A[ind]
    t = cv2.merge([t, t, t])
    res = (im - A) / t + A
    return res


def dehaze(src, sz=15, bGamma=False):
    src = np.float32(src) / 255
    dark = DarkChannel(src, sz)
    A = AtmLight(src, dark)
    te = TransmissionEstimate(src, A, sz)
    # A = AirlightEstimation(src)
    # te = TransmissionEstimateNew(src,A,sz)
    tr = TransmissionRefine(src, te)
    res = RestoreImg(src, tr, A)
    res = np.clip(res * 255, 1, 255).astype(np.uint8)
    # Gamma校正--改善去雾后图像变暗
    if bGamma:
        res = gamma_trans(res, gamma=0.5)
    return res


def video_dehaze():
    sz = 9
    cap = cv2.VideoCapture('./img/haze_video.mp4')
    while (cap.isOpened()):
        ret, frame = cap.read()
        dest = dehaze(frame, sz, False)
        cv2.imshow('frame', dest)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # video_dehaze()

    sz = 9
    bGamma = False
    src = cv2.imread("./img/canon.bmp")
    # src = cv2.resize(src, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    dest = dehaze(src, sz, bGamma)
    contrast = np.hstack((src, dest))
    cv2.imwrite('./img/canon_dehaze.jpg', dest)
    cv2.imshow("contrast", contrast)
