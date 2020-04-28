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
from offlineTask.models import OfflineTask, SingleImageInfo, SingleImageIdentifyInfo


def handleHtmlImages(resultId):
    global isAllImagehandle
    users = OfflineTask.objects.all()
    singleImages = SingleImageInfo.objects.all()
    singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
    singleImage_dict = {}

    for user in users:
        if user.id == int(resultId):
            for singleImage in singleImages:
                isAllImagehandle = True
                if singleImage.begin >= user.begin \
                        and singleImage.overDate == user.overDate\
                        and singleImage.is_show == False:
                    for singleImageIdentify in singleImageIdentifys:
                        if singleImageIdentify.singleImageId == singleImage.id:
                            isAllImagehandle = False
                            singleImage_dict[singleImage.id] = {
                                "userId": user.id,
                                "singleImageId": singleImage.id,
                                "singleImageName": singleImageIdentify.title,
                                "icon_originUrl": "/static/upload/" + singleImageIdentify.imagePreprocessPath,
                                "icon_predictUrl": "/static/upload/" + singleImageIdentify.imageIdentifyPath,
                            }
                            singleImage.is_show = True
                            singleImage.save()
                            break
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
        singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.singleImageId == int(singleImageId):
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
            if singleImageIdentify.singleImageId == int(singleImageId):
                singleImageIdentify.is_confirm = False
                singleImageIdentify.save()
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


