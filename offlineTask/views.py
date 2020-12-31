import datetime
import json
import os
import shutil
import tkinter
import uuid
import numpy as np
import cv2
import jinja2

from PIL import Image, ImageTk
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt
from docx.shared import Mm, Inches, Pt
from docxtpl import DocxTemplate, InlineImage

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from image_preprocess import getImgList
from offlineTask.models import OfflineTask, SingleImagePreprocessInfo, SingleImageIdentifyInfo, SingleImageSpliceInfo, \
    SingleImageCompareInfo, OfflinePreprocessSet


def copy(path,path1):                       #path原文件地址，path1指定地址
    fp = open(path,'rb')
    fp1 = open(path1,'wb')

    for i in fp:
        fp1.write(i)                        #向新文件中写入数据
    fp.close()
    fp1.close()

class show_sliced_images:
    def __init__(self, load_path, slice_size):
        self.load_path = load_path
        self.slice_size = slice_size
        self.img_tk = None
        self.slice_name_set = set([f for f in os.listdir(self.load_path) if f.endswith(".jpg")])

        # 窗口和标题
        window = tkinter.Tk()
        window.title("查看高清图片")

        # 打包一个黑色画布到窗口
        self.canvas = tkinter.Canvas(window, width=self.slice_size[1] * 2, height=self.slice_size[0] * 2, bg="black")
        self.canvas.focus_set()  # 让画布获得焦点,对于键盘
        self.canvas.pack()

        # 绑定键盘事件，交由processKeyboardEvent函数去处理，事件对象会作为参数传递给该函数
        self.canvas.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.canvas.bind(sequence="<MouseWheel>", func=self.processMouseWheelEvent)

        # 初始化时，显示左上角切片
        self.row_col_nums = 5
        self.current_pos = (0, 0)
        self.redraw(self.current_pos, self.row_col_nums)

        # 消息循环
        window.mainloop()

    def redraw(self, input_pos, row_col_nums):
        img = np.zeros((row_col_nums * self.slice_size[0], row_col_nums * self.slice_size[1], 3), np.uint8)
        for i in range(row_col_nums):
            for j in range(row_col_nums):
                slice_name = str(input_pos[0] + i) + "-" + str(input_pos[1] + j) + ".jpg"
                if slice_name in self.slice_name_set:
                    #slice_img = cv2.imread(self.load_path + slice_name)
                    slice_img = cv2.imdecode(np.fromfile(self.load_path + slice_name, dtype=np.uint8), 1)
                    img[i * self.slice_size[0]:(i + 1) * self.slice_size[0], j * self.slice_size[1]:(j + 1) * self.slice_size[1]] = slice_img
        if row_col_nums > 2:
            img = cv2.resize(img, (2 * self.slice_size[1], 2 * self.slice_size[0]), interpolation=cv2.INTER_AREA)
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        self.img_tk = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(self.slice_size[1], self.slice_size[0], image=self.img_tk)

    def processKeyboardEvent(self, event):
        new_pos = self.current_pos
        if event.keysym == "Down":
            new_pos = (self.current_pos[0] + 1, self.current_pos[1])
        elif event.keysym == "Up":
            new_pos = (self.current_pos[0] - 1, self.current_pos[1])
        elif event.keysym == "Left":
            new_pos = (self.current_pos[0], self.current_pos[1] - 1)
        elif event.keysym == "Right":
            new_pos = (self.current_pos[0], self.current_pos[1] + 1)
        else:
            pass

        if new_pos != self.current_pos:
            img0 = str(new_pos[0]) + "-" + str(new_pos[1]) + ".jpg"
            if img0 in self.slice_name_set:
                self.current_pos = new_pos
                self.redraw(self.current_pos, self.row_col_nums)

    def processMouseWheelEvent(self, event):
        new_row_col_nums = self.row_col_nums

        if event.delta > 0:
            # 滚轮往上滚动，放大
            if new_row_col_nums > 2:
                new_row_col_nums -= 1
        elif event.delta < 0:
            # 滚轮往下滚动，缩小
            if new_row_col_nums < 9:
                new_row_col_nums += 1
        else:
            pass

        if new_row_col_nums != self.row_col_nums:
            self.row_col_nums = new_row_col_nums
            self.redraw(self.current_pos, self.row_col_nums)

def spliceHtmlImages(resultId):
    users = OfflineTask.objects.all()

    singleImageSpliceInfos = SingleImageSpliceInfo.objects.all()
    singleSpliceImage_dict = {}

    for user in users:
        if user.id == int(resultId):
            for singleImageSpliceInfo in singleImageSpliceInfos:
                if singleImageSpliceInfo.overDate == user.overDate:
                    singleSpliceImage_dict[singleImageSpliceInfo.id] = {
                        "userId": user.id,
                        "singleImageSpliceId": singleImageSpliceInfo.id,
                        "singleImageName": singleImageSpliceInfo.titleId,
                        "icon_spliceUrl": "/static/upload/" + singleImageSpliceInfo.imageSplicePath,
                    }

                    singleImageSpliceInfo.is_show = True
                    singleImageSpliceInfo.save()
                    break
            break
    singleSpliceImage_list = list(six.itervalues(singleSpliceImage_dict))
    context = dict(
        singleSpliceImages=singleSpliceImage_list,
    )
    return context

def preprocessHtmlImages(resultId, singlePreprocessImageId, isNext):
    users = OfflineTask.objects.all()

    singleImagePreprocesss = SingleImagePreprocessInfo.objects.all()
    singlePreprocessImage_dict = {}
    singlePreprocesshint_dict = {}
    isAllShown = True

    for user in users:
        if user.id == int(resultId):
            for singleImagePreprocess in singleImagePreprocesss:
                if singleImagePreprocess.overDate == user.overDate and \
                        ((singlePreprocessImageId != None and singleImagePreprocess.id == int(singlePreprocessImageId))
                                or singlePreprocessImageId is None):
                    isAllShown = False
                    singlePreprocessImage_dict[singleImagePreprocess.id] = {
                        "userId": user.id,
                        "singleImagePreprocessId": singleImagePreprocess.id,
                        "singleImageName": singleImagePreprocess.titleId,
                        "icon_preprocessUrl": "/static/upload/" + singleImagePreprocess.imagePreprocessPath,
                        "icon_originUrl": "/static/upload/" + singleImagePreprocess.imageOriginPath,
                    }

                    singleImagePreprocess.is_show = True
                    singleImagePreprocess.save()
                    break
            if  isAllShown:
                singlePreprocesshint_dict[user.id] = {
                    "isNext": isNext,
                    "singleImagePreprocessId": singlePreprocessImageId,
                    "userId": int(resultId),
                    "userStatus": user.preprocess_status
                }
            break
    singlePreprocessImage_list = list(six.itervalues(singlePreprocessImage_dict))
    singlePreprocesshint_list = list(six.itervalues(singlePreprocesshint_dict))
    context = dict(
        singlePreprocessImages=singlePreprocessImage_list,
        singlePreprocesshints= singlePreprocesshint_list,
    )
    return context

def comparisonHtmlImages(resultId, singleCompareImageId, isNext):
    users = OfflineTask.objects.all()

    singleImageCompareInfos = SingleImageCompareInfo.objects.all()
    singleCompareImage_dict = {}
    singleComparehint_dict = {}
    isAllShown = True

    for user in users:
        if user.id == int(resultId):
            for singleImageCompareInfo in singleImageCompareInfos:
                if singleImageCompareInfo.overDate == user.overDate and \
                        ((singleCompareImageId != None and singleImageCompareInfo.id == int(singleCompareImageId))
                                or singleCompareImageId is None) and singleImageCompareInfo.is_show != 2:
                    isAllShown = False
                    singleCompareImage_dict[singleImageCompareInfo.id] = {
                        "userId": user.id,
                        "singleImageCompareId": singleImageCompareInfo.id,
                        "singleImageName": singleImageCompareInfo.titleId,
                        "icon_originPartUrl": "/static/upload/" + singleImageCompareInfo.imageComOriginPartPath,
                        "icon_originPanoUrl": "/static/upload/" + singleImageCompareInfo.imageComOriginPanoPath,
                        "icon_originResultUrl": "/static/upload/" + singleImageCompareInfo.imageComOriginResultPath,
                    }

                    singleImageCompareInfo.is_show = True
                    singleImageCompareInfo.save()
                    break
            if  isAllShown:
                singleComparehint_dict[user.id] = {
                    "isNext": isNext,
                    "singleImageCompareId": singleCompareImageId,
                    "userId": int(resultId),
                    "userStatus": user.comparison_status
                }
            break
    singleCompareImage_list = list(six.itervalues(singleCompareImage_dict))
    singleComparehint_list = list(six.itervalues(singleComparehint_dict))
    context = dict(
        singleCompareImages=singleCompareImage_list,
        singleComparehints= singleComparehint_list,
    )
    return context

def identifyHtmlImages(resultId, singleIdentifyImageId, isNext):
    users = OfflineTask.objects.all()

    singleImageIdentifyInfos = SingleImageIdentifyInfo.objects.all()
    singleIdentifyImage_dict = {}
    singleIdentifyhint_dict = {}
    isAllShown = True

    for user in users:
        if user.id == int(resultId):
            for singleImageIdentifyInfo in singleImageIdentifyInfos:
                if singleImageIdentifyInfo.overDate == user.overDate and \
                        ((singleIdentifyImageId != None and singleImageIdentifyInfo.id == int(singleIdentifyImageId))
                         or singleIdentifyImageId is None):
                    isAllShown = False
                    singleIdentifyImage_dict[singleImageIdentifyInfo.id] = {
                        "userId": user.id,
                        "singleImageIdentifyId": singleImageIdentifyInfo.id,
                        "singleImageName": singleImageIdentifyInfo.titleId,
                        "icon_preprocessUrl": "/static/upload/" + singleImageIdentifyInfo.imagePreprocessPath,
                        "icon_identifyUrl": "/static/upload/" + singleImageIdentifyInfo.imageIdentifyPath,
                    }

                    singleImageIdentifyInfo.is_show = True
                    singleImageIdentifyInfo.save()
                    break
            if isAllShown:
                singleIdentifyhint_dict[user.id] = {
                    "isNext": isNext,
                    "singleImageIdentifyId": singleIdentifyImageId,
                    "userId": int(resultId),
                    "userStatus": user.identify_status
                }
            break
    singleIdentifyImage_list = list(six.itervalues(singleIdentifyImage_dict))
    singleIdentifyhint_list = list(six.itervalues(singleIdentifyhint_dict))
    context = dict(
        singleIdentifyImages=singleIdentifyImage_list,
        singleIdentifyhints=singleIdentifyhint_list,
    )
    return context

def identifyConfirm(request, userId,singleImageIdentifyId):
    isNext = None
    singleImageIdentifyIdInt = 0
    if 'predict_confirm' in request.POST:
        singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                singleImageIdentify.is_confirm = True
                #overdate = datetime.datetime.now().strftime("%Y/%m/icons")
                singleImageIdentify.imageIdentifyResultPath = singleImageIdentify.imageIdentifyPath.replace('identify','identifyResult')
                #用绝对路径创建确认结果的文件夹
                identify_path =os.path.dirname(singleImageIdentify.imageIdentifyResultPath)
                if not os.path.exists(identify_path):
                    os.makedirs(identify_path)
                shutil.copy(singleImageIdentify.imageIdentifyPath, singleImageIdentify.imageIdentifyResultPath)
                singleImageIdentify.save()
                singleImageIdentifyIdInt = int(singleImageIdentifyId) + 1
                isNext = True
                break
        pass
    elif 'predict_cancel' in request.POST:
        singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                singleImageIdentify.is_confirm = False
                if singleImageIdentify.imageIdentifyResultPath is not None \
                    and (os.path.exists(singleImageIdentify.imageIdentifyResultPath)):
                    shutil.rmtree(singleImageIdentify.imageIdentifyResultPath)
                singleImageIdentify.imageIdentifyResultPath = None
                singleImageIdentify.save()
                singleImageIdentifyIdInt = int(singleImageIdentifyId) + 1
                isNext = True
                break
        pass
    #测试提交代码
    elif 'predict_next' in request.POST:
        singleImageIdentifyIdInt = int(singleImageIdentifyId) + 1
        isNext = True
    elif 'predict_pre' in request.POST:
        singleImageIdentifyIdInt = int(singleImageIdentifyId) - 1
        isNext = False
    context = identifyHtmlImages(userId, singleImageIdentifyIdInt, isNext)
    return render(request, 'identifyResult.html', context)

def preprocessConfirm(request, userId, singlePreprocessImageId):
    isNext = None
    singlePreprocessImageIdInt = 0
    if 'predict_next' in request.POST:
        singlePreprocessImageIdInt = int(singlePreprocessImageId) + 1
        isNext = True
    elif 'predict_pre' in request.POST:
        singlePreprocessImageIdInt = int(singlePreprocessImageId) - 1
        isNext = False
    context = preprocessHtmlImages(userId, singlePreprocessImageIdInt, isNext)
    return render(request, 'preprocessResult.html', context)

def comparisonConfirm(request, userId, singleComparisonImageId):
    isNext = None
    singleCompareImageIdInt = 0
    if 'predict_next' in request.POST:
        if singleComparisonImageId != 'None' and singleComparisonImageId is not None:
            singleCompareImageIdInt = int(singleComparisonImageId) + 1
        else:
            singleCompareImageIdInt = None
        isNext = True
    elif 'predict_pre' in request.POST:
        if singleComparisonImageId != 'None' and singleComparisonImageId is not None:
            singleCompareImageIdInt = int(singleComparisonImageId) - 1
        else:
            singleCompareImageIdInt = None
        isNext = False
    context = comparisonHtmlImages(userId, singleCompareImageIdInt, isNext)
    return render(request, 'comparisonResult.html', context)

def spliceConfirm(request,userId,singleSpliceImageId):
    if 'splice_detail' in request.POST:
        singleSpliceImages = SingleImageSpliceInfo.objects.all()
        for singleSpliceImage in singleSpliceImages:
            if singleSpliceImage.id == int(singleSpliceImageId):
                save_path, file = os.path.split(singleSpliceImage.imageSplicePath)
                slice_size = (400, 640)
                show_sliced_images(save_path+'/', slice_size)
    context = spliceHtmlImages(userId)
    return render(request, 'spliceResult.html', context)

def identifyResult(request,resultId):
    print(resultId)
    context = identifyHtmlImages(resultId, None, None)
    return render(request, 'identifyResult.html', context)

def spliceResult(request,resultId):
    context = spliceHtmlImages(resultId)
    return render(request, 'spliceResult.html', context)

def preprocessResult(request,resultId):
    context = preprocessHtmlImages(resultId,None,None)
    return render(request, 'preprocessResult.html', context)

def comparisonResult(request,resultId):
    context = comparisonHtmlImages(resultId,None,None)
    return render(request, 'comparisonResult.html', context)

@login_required
@csrf_exempt
def upload_temp_image(request):
    result = {}
    if request.method == 'POST':
        files = request.FILES
        if files:
            image_url_list = []
            for file_name in files:
                image_url_list.append(handle_uploaded_file(files.get(file_name)))  # 处理上传文件
            result = {'msg': 'success', "image_list": image_url_list, }

        else:
            result = {'msg': 'failed', "image_list": []}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")  # 返回json

# 处理上传的文件
def handle_uploaded_file(file):
    # 分割文件名，提取拓展名
    extension = os.path.splitext(file.name)
    # 使用uuid4重命名文件，防止重名文件相互覆盖
    #注意首先在项目的根目录下新建media/tempimg，或者自己使用python代码创建目录
    #file_name = '{}{}'.format(uuid.uuid4(), extension[1])
    with open(TEMP_IMAGE_DIR + file.name, 'wb+') as destination:
        for chunk in file.chunks():#防止文件太大导致内存溢出
            destination.write(chunk)
    # 返回图片的URL
    return os.path.join(WEB_HOST_MEDIA_URL, file.name)

def read_file(file_name, size):
    with open(file_name,mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break

def download(request, userId):
    #file_path = 'D:\202006115wjk\topic'
    pStatus = ''
    identifyStatus = ''
    cStatus = ''
    spliceStatus = ''
    overDate = ''
    beginTime = ''
    creator = ''
    #preImgs = []
    #idImgs = []
    #comImgs = []
    #spImgs = []
    preImgsTemp = []
    idImgsTemp = []
    comImgsTemp = []
    spImgsTemp = []

    filename = 'test.docx'
    filepath = 'D:\\202006115wjk\\topic\\download\\'
    template_path = os.getcwd() + '\\train.docx'
    template = DocxTemplate(template_path)
    users = OfflineTask.objects.all()
    singleImagePreprocessInfos = SingleImagePreprocessInfo.objects.all()
    singleImageIdentifyInfos = SingleImageIdentifyInfo.objects.all()
    singleImageSpliceInfos = SingleImageSpliceInfo.objects.all()
    singleImageCompareInfos = SingleImageCompareInfo.objects.all()

    for user in users:
        if user.id == int(userId):
            overDate = user.overDate
            beginTime = user.begin
            creator = user.creator
            identifyStatus = user.identify_status
            spliceStatus = user.splice_status
            pStatus = user.preprocess_status
            cStatus = user.comparison_status
            break

    context = {}
    try:
        context = {
                    'beginTime': beginTime,
                    'creator': creator,
                    'identifyStatus': identifyStatus,
                    'spliceStatus': spliceStatus,
                    'pStatus': pStatus,
                    'cStatus': cStatus,
        }
    except Exception as e:
        print(e)

    if pStatus == 'd':
        for singleImagePreprocessInfo in singleImagePreprocessInfos :
            if singleImagePreprocessInfo.overDate == overDate \
                    and singleImagePreprocessInfo.imagePreprocessPath != None\
                    and singleImagePreprocessInfo.imagePreprocessPath != '':
                    preImgsTemp.append({'image': InlineImage(template,singleImagePreprocessInfo.imagePreprocessPath,width=Mm(80), height=Mm(60))})
        context['pre_list']=preImgsTemp

    if identifyStatus == 'd':
        for singleImageIdentifyInfo in singleImageIdentifyInfos:
            if singleImageIdentifyInfo.overDate == overDate \
                    and singleImageIdentifyInfo.imageIdentifyResultPath != None \
                    and singleImageIdentifyInfo.imageIdentifyResultPath != '':
                    idImgsTemp.append({'image': InlineImage(template,singleImageIdentifyInfo.imageIdentifyResultPath,width=Mm(80), height=Mm(60))})
        context['iden_list'] = idImgsTemp

    if cStatus == 'd':
        for singleImageCompareInfo in singleImageCompareInfos:
            if singleImageCompareInfo.overDate == overDate \
                    and singleImageCompareInfo.imageComOriginResultPath != None\
                    and singleImageCompareInfo.imageComOriginResultPath != '':
                comImgsTemp.append({'image1': InlineImage(template,singleImageCompareInfo.imageComOriginResultPath,width=Mm(80), height=Mm(60)),
                                    'image2': InlineImage(template,singleImageCompareInfo.imageComOriginPartPath,width=Mm(80), height=Mm(60))})
        context['com_list'] = comImgsTemp

    if spliceStatus == 'd':
        for singleImageSpliceInfo in singleImageSpliceInfos:
            if singleImageSpliceInfo.overDate == overDate \
                    and singleImageSpliceInfo.imageSplicePath != None\
                    and singleImageSpliceInfo.imageSplicePath != '':
                    spImgsTemp.append({'image': InlineImage(template,singleImageSpliceInfo.imageSplicePath,width=Mm(80), height=Mm(60))})
        context['splice_list'] = spImgsTemp

    jinja_env = jinja2.Environment(autoescape=True)
    template.render(context, jinja_env)
    template.save(os.path.join(filepath, filename))
    response = StreamingHttpResponse(read_file(os.path.join(filepath, filename),512))
    response['Content-Type']='application/msword'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    return response