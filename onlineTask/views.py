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

from onlineTask.models import OnlineTask, OnlineImageIdentifyInfo
from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from offlineTask.models import OfflineTask, SingleImageIdentifyInfo, SingleImagePreprocessInfo

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

def preprocessHtmlImages(resultId, singlePreprocessImageId, isNext):
    users = OnlineTask.objects.all()

    onlineImageIdentifyInfos = OnlineImageIdentifyInfo.objects.all()
    singlePreprocessImage_dict = {}
    singlePreprocesshint_dict = {}
    isAllShown = True

    for user in users:
        if user.id == int(resultId):
            for onlineImageIdentifyInfo in onlineImageIdentifyInfos:
                if onlineImageIdentifyInfo.overDate == user.overDate and \
                        ((singlePreprocessImageId != None and onlineImageIdentifyInfo.id == int(singlePreprocessImageId))
                                or singlePreprocessImageId is None):
                    isAllShown = False
                    singlePreprocessImage_dict[onlineImageIdentifyInfo.id] = {
                        "userId": user.id,
                        "singleImagePreprocessId": onlineImageIdentifyInfo.id,
                        "singleImageName": onlineImageIdentifyInfo.title,
                        "icon_preprocessUrl": "/static/upload/" + onlineImageIdentifyInfo.imagePreprocessPath,
                        "icon_originUrl": "/static/upload/" + onlineImageIdentifyInfo.imageOriginPath,
                    }

                    onlineImageIdentifyInfo.is_show = True
                    onlineImageIdentifyInfo.save()
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
    return render(request, 'preprocessOnlineResult.html', context)

def identifyResult(request,resultId):
    print(resultId)
    context = identifyHtmlImages(resultId)
    return render(request, 'identifyResult.html', context)

def preprocessResult(request,resultId):
    context = preprocessHtmlImages(resultId,None,None)
    return render(request, 'preprocessOnlineResult.html', context)