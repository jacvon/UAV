import datetime
import json
import os
import string
import uuid
from os import mkdir
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from preprocess.models import PreprocessTask, SingleImageInfo


def handleHtmlImages(resultId):
    global isAllImagehandle
    users = PreprocessTask.objects.all()
    singleImages = SingleImageInfo.objects.all()
    singleImage_dict = {}

    for user in users:
        if user.id == int(resultId):
            for singleImage in singleImages:
                isAllImagehandle = True
                if singleImage.begin >= user.begin and singleImage.title == user.title and singleImage.is_show == False:
                    isAllImagehandle = False
                    singleImage_dict[singleImage.id] = {
                        "userId": user.id,
                        "singleImageId": singleImage.id,
                        "singleImageName": singleImage.title,
                        "icon_originUrl": "/static/upload/" + singleImage.imageOriginPath,
                        "icon_predictUrl": "/static/upload/" + singleImage.imageIdentifyPath,
                    }
                    singleImage.is_show = True
                    singleImage.save()
                    break
            if isAllImagehandle:
                user.identify_status = 'd'
                user.save()
            break
    singleImage_list = list(six.itervalues(singleImage_dict))
    context = dict(
        singleImages = singleImage_list,
    )
    return context


def copy(path,path1):                       #path原文件地址，path1指定地址
    fp = open(path,'rb')
    fp1 = open(path1,'wb')

    for i in fp:
        fp1.write(i)                        #向新文件中写入数据
    fp.close()
    fp1.close()

def predict_confirm(request, userId,singleImageId):
    if 'predict_confirm' in request.POST:
        singleImages = SingleImageInfo.objects.all()
        for singleImage in singleImages:
            if singleImage.id == int(singleImageId):
                singleImage.is_confirm = True
                #overdate = datetime.datetime.now().strftime("%Y/%m/icons")
                #存储相对路径
                singleImage.imageIdentifyResultPath = '%s/%s/%s/%s' % (singleImage.title, singleImage.overDate,'identifyResult',singleImage.imageOriginPath.split('/')[-1])
                #用绝对路径创建确认结果的文件夹
                identifyResult_folder= '%s/%s/%s/%s/%s' % (BASE_DIR, 'static/upload',singleImage.title, singleImage.overDate,'identifyResult')
                if not os.path.exists(identifyResult_folder):
                    os.makedirs(identifyResult_folder)
                #需要绝对路径来执行copy操作
                predict_path = '%s/%s/%s' % (BASE_DIR, 'static/upload',singleImage.imagePreprocessPath)
                result_path = '%s/%s/%s' % (BASE_DIR, 'static/upload',singleImage.imageIdentifyResultPath)
                copy(predict_path, result_path)
                singleImage.save()
                break
        pass
    elif 'predict_cancel' in request.POST:
        singleImages = SingleImageInfo.objects.all()
        for singleImage in singleImages:
            if singleImage.id == int(singleImageId):
                singleImage.is_confirm = False
                singleImage.save()
                break
        pass
    #测试提交代码
    context = handleHtmlImages(userId)
    return render(request, 'predict_result.html', context)


def image_predict(request,resultId):
    print(resultId)
    context = handleHtmlImages(resultId)
    return render(request, 'predict_result.html', context)

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
    file_name = '{}{}'.format(uuid.uuid4(), extension[1])
    with open(TEMP_IMAGE_DIR + file_name, 'wb+') as destination:
        for chunk in file.chunks():#防止文件太大导致内存溢出
            destination.write(chunk)
    # 返回图片的URL
    return os.path.join(WEB_HOST_MEDIA_URL, file_name)


