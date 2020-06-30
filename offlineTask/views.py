import datetime
import json
import os
import tkinter
import uuid

from PIL import Image, ImageTk
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from offlineTask.models import OfflineTask, SingleImagePreprocessInfo, SingleImageIdentifyInfo, SingleImageSpliceInfo, SingleImageCompareInfo


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
        self.name_list = [f for f in os.listdir(self.load_path) if f.endswith(".jpg")]

        # 窗口和标题
        window = tkinter.Tk()
        window.title("显示切片图片")

        # 打包一个白色画布到窗口
        self.canvas = tkinter.Canvas(window, width=self.slice_size[1] * 2, height=self.slice_size[0] * 2, bg="black")
        self.canvas.focus_set()  # 让画布获得焦点,对于键盘
        self.canvas.pack()

        # 绑定键盘事件，交由processKeyboardEvent函数去处理，事件对象会作为参数传递给该函数
        self.canvas.bind(sequence="<Key>", func=self.processKeyboardEvent)

        # 初始化 self.img_tk（list_size=4）
        img_open = Image.open(self.load_path + "0-0.jpg")
        self.img_tk = [ImageTk.PhotoImage(img_open) for i in range(4)]

        # 初始化时，显示默认图片
        self.current_pos = (0, 0)
        self.redraw(self.current_pos)

        # 消息循环
        window.mainloop()

    def redraw(self, input_pos):
        img_left_up = str(input_pos[0]) + "-" + str(input_pos[1]) + ".jpg"
        img_right_down = str(input_pos[0] + 1) + "-" + str(input_pos[1] + 1) + ".jpg"

        # 当且仅当左上和右下切片图像存在时才进行重绘
        if (img_left_up in self.name_list) and (img_right_down in self.name_list):
            img_left_down = str(input_pos[0] + 1) + "-" + str(input_pos[1]) + ".jpg"
            img_right_up = str(input_pos[0]) + "-" + str(input_pos[1] + 1) + ".jpg"

            # 将相邻的四张切片图像显示在画布（注意画布上锚点位置是各切片图的中心）
            img_open = Image.open(self.load_path + img_left_up)
            self.img_tk[0] = ImageTk.PhotoImage(img_open)
            self.canvas.create_image(self.slice_size[1] // 2, self.slice_size[0] // 2, image=self.img_tk[0])

            img_open = Image.open(self.load_path + img_left_down)
            self.img_tk[1] = ImageTk.PhotoImage(img_open)
            self.canvas.create_image(self.slice_size[1] // 2, 3 * self.slice_size[0] // 2, image=self.img_tk[1])

            img_open = Image.open(self.load_path + img_right_up)
            self.img_tk[2] = ImageTk.PhotoImage(img_open)
            self.canvas.create_image(3 * self.slice_size[1] // 2, self.slice_size[0] // 2, image=self.img_tk[2])

            img_open = Image.open(self.load_path + img_right_down)
            self.img_tk[3] = ImageTk.PhotoImage(img_open)
            self.canvas.create_image(3 * self.slice_size[1] // 2, 3 * self.slice_size[0] // 2, image=self.img_tk[3])

            self.current_pos = input_pos

    def processKeyboardEvent(self, ke):
        input_pos = self.current_pos

        if ke.keysym == "Down":
            input_pos = (self.current_pos[0] + 1, self.current_pos[1])
        elif ke.keysym == "Up":
            input_pos = (self.current_pos[0] - 1, self.current_pos[1])
        elif ke.keysym == "Left":
            input_pos = (self.current_pos[0], self.current_pos[1] - 1)
        elif ke.keysym == "Right":
            input_pos = (self.current_pos[0], self.current_pos[1] + 1)
        else:
            pass

        if input_pos != self.current_pos:
            self.redraw(input_pos)

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
                                or singleCompareImageId is None):
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

def identifyHtmlImages(resultId):
    users = OfflineTask.objects.all()

    singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
    singleIdentifyImage_dict = {}

    for user in users:
        if user.id == int(resultId):
            for singleImageIdentify in singleImageIdentifys:
                if singleImageIdentify.overDate == user.overDate:
                    singleIdentifyImage_dict[singleImageIdentify.id] = {
                        "userId": user.id,
                        "singleImageIdentifyId": singleImageIdentify.id,
                        "singleImageName": singleImageIdentify.title,
                        "icon_preprocessUrl": "/static/upload/" + singleImageIdentify.imagePreprocessPath,
                        "icon_identifyUrl": "/static/upload/" + singleImageIdentify.imageIdentifyPath,
                        }

                    singleImageIdentify.is_show = True
                    singleImageIdentify.save()
                    break
            break
    singleIdentifyImage_list = list(six.itervalues(singleIdentifyImage_dict))
    context = dict(
        singleIdentifyImages = singleIdentifyImage_list,
    )
    return context

def identifyConfirm(request, userId,singleImageIdentifyId):
    if 'predict_confirm' in request.POST:
        singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                singleImageIdentify.is_confirm = True
                #overdate = datetime.datetime.now().strftime("%Y/%m/icons")
                #存储相对路径
                singleImageIdentify.imageIdentifyResultPath = '%s/%s/%s/%s' % (singleImageIdentify.title, singleImageIdentify.overDate,'identifyResult',singleImageIdentify.imagePreprocessPath.split('/')[-1])
                #用绝对路径创建确认结果的文件夹
                identifyResult_folder= '%s/%s/%s/%s/%s' % (BASE_DIR, 'static/upload',singleImageIdentify.title, singleImageIdentify.overDate,'identifyResult')
                if not os.path.exists(identifyResult_folder):
                    os.makedirs(identifyResult_folder)
                #需要绝对路径来执行copy操作
                predict_path = '%s/%s/%s' % (BASE_DIR, 'static/upload',singleImageIdentify.imagePreprocessPath)
                result_path = '%s/%s/%s' % (BASE_DIR, 'static/upload',singleImageIdentify.imageIdentifyResultPath)
                copy(predict_path, result_path)
                singleImageIdentify.save()
                break
        pass
    elif 'predict_cancel' in request.POST:
        singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                singleImageIdentify.is_confirm = False
                singleImageIdentify.save()
                break
        pass
    #测试提交代码
    context = identifyHtmlImages(userId)
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
        singleCompareImageIdInt = int(singleComparisonImageId) + 1
        isNext = True
    elif 'predict_pre' in request.POST:
        singleCompareImageIdInt = int(singleComparisonImageId) - 1
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
    context = identifyHtmlImages(resultId)
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