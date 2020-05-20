import datetime
import json
import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from offlineTask.models import OfflineTask, SingleImagePreprocessInfo, SingleImageIdentifyInfo, SingleImageSpliceInfo


def copy(path,path1):                       #path原文件地址，path1指定地址
    fp = open(path,'rb')
    fp1 = open(path1,'wb')

    for i in fp:
        fp1.write(i)                        #向新文件中写入数据
    fp.close()
    fp1.close()

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
                        "singleImageName": singleImageSpliceInfo.title,
                        "icon_preprocessUrl": "/static/upload/" + singleImageSpliceInfo.imagePreprocessPath,
                        "icon_spliceUrl": "/static/upload/" + singleImageSpliceInfo.imageSplicePath,
                    }
                    if singleImageSpliceInfo.progress == 1:
                        user.preprocess_status = 'd'
                        user.save()
                    singleImageSpliceInfo.is_show = True
                    singleImageSpliceInfo.save()
                    break
            break
    singleSpliceImage_list = list(six.itervalues(singleSpliceImage_dict))
    context = dict(
        singleSpliceImages=singleSpliceImage_list,
    )
    return context

def preprocessHtmlImages(resultId):
    users = OfflineTask.objects.all()

    singleImagePreprocesss = SingleImagePreprocessInfo.objects.all()
    singlePreprocessImage_dict = {}

    for user in users:
        if user.id == int(resultId):
            for singleImagePreprocess in singleImagePreprocesss:
                if singleImagePreprocess.overDate == user.overDate:
                    singlePreprocessImage_dict[singleImagePreprocess.id] = {
                        "userId": user.id,
                        "singleImagePreprocessId": singleImagePreprocess.id,
                        "singleImageName": singleImagePreprocess.title,
                        "icon_preprocessUrl": "/static/upload/" + singleImagePreprocess.imagePreprocessPath,
                        "icon_originUrl": "/static/upload/" + singleImagePreprocess.imageOriginPath,
                    }
                    if singleImagePreprocess.progress == 1:
                        user.preprocess_status = 'd'
                        user.save()
                    singleImagePreprocess.is_show = True
                    singleImagePreprocess.save()
                    break
            break
    singlePreprocessImage_list = list(six.itervalues(singlePreprocessImage_dict))
    context = dict(
        singlePreprocessImages=singlePreprocessImage_list,
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
                    if singleImageIdentify.progress == 1:
                        user.identify_status = 'd'
                        user.save()
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

def preprocessConfirm(request,userId, singlePreprocessImageId):
    print(userId)
    print(singlePreprocessImageId)
    return None

def spliceConfirm(request,userId,singleSpliceImageId):
    print(userId)
    print(singleSpliceImageId)
    return None

def identifyResult(request,resultId):
    print(resultId)
    context = identifyHtmlImages(resultId)
    return render(request, 'identifyResult.html', context)

def spliceResult(request,resultId):
    print(resultId)
    context = spliceHtmlImages(resultId)
    return render(request, 'spliceResult.html', context)

def preprocessResult(request,resultId):
    print(resultId)
    context = preprocessHtmlImages(resultId)
    return render(request, 'identifyResult.html', context)

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