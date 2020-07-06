import datetime
import json
import os
import tkinter
import uuid
import numpy as np
import cv2

from PIL import Image, ImageTk
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from offlineTask.models import OfflineTask,  SingleImageIdentifyInfo

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

def identifyResult(request,resultId):
    print(resultId)
    context = identifyHtmlImages(resultId)
    return render(request, 'identifyResult.html', context)
