import datetime
import json
import os
import shutil
import tkinter
import uuid
import socket

import numpy as np
import cv2

from PIL import Image, ImageTk
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import six
from django.views.decorators.csrf import csrf_exempt

from image_stitch import get_gps
from onlineTask.models import OnlineTask, OnlineImageIdentifyInfo
from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR, WEB_HOST_MEDIA_URL
from offlineTask.models import OfflineTask, SingleImageIdentifyInfo

def transBack(flyBackImagePath):
    gps = get_gps(flyBackImagePath)
    print(gps)
    #transJson = 'long123:' + str(gps[0][0]) + ',lat:' + str(gps[0][1]) + ',alt:' + str(gps[0][2])
    transJson = {
                "MessageType": "AssignGPS",
                "longitude": str(gps[0][0]),
                "latitude": str(gps[0][1]),
                "altitude": str(gps[0][2])}
    print(gps,transJson)
    client = socket.socket()
    client.connect(('127.0.0.1', 8888))
    client.send(json.dumps(transJson).encode())
    data = client.recv(1024)  # 这里是字节1k
def identifyHtmlImages(resultId, singleIdentifyImageId, isNext):
    users = OnlineTask.objects.all()

    singleImageIdentifyInfos  = OnlineImageIdentifyInfo.objects.all()
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
                        "singleImageName": singleImageIdentifyInfo.title,
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
    isNext = None
    singleImageIdentifyIdInt = 0
    if 'predict_confirm' in request.POST:
        singleImageIdentifys = OnlineImageIdentifyInfo.objects.all()
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
                break
        pass
    elif 'predict_cancel' in request.POST:
        singleImageIdentifys = OnlineImageIdentifyInfo.objects.all()
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                singleImageIdentify.is_confirm = False
                if singleImageIdentify.imageIdentifyResultPath is not None \
                    and (os.path.exists(singleImageIdentify.imageIdentifyResultPath)):
                    os.remove(singleImageIdentify.imageIdentifyResultPath)
                singleImageIdentify.imageIdentifyResultPath = None
                singleImageIdentify.save()
                singleImageIdentifyIdInt = int(singleImageIdentifyId) + 1
                break
        pass
    #测试提交代码
    elif 'predict_next' in request.POST:
        singleImageIdentifyIdInt = int(singleImageIdentifyId) + 1
        isNext = True
    elif 'predict_pre' in request.POST:
        singleImageIdentifyIdInt = int(singleImageIdentifyId) - 1
        isNext = False
    elif 'fly_back' in request.POST:
        flyBackImagePath = None
        singleImageIdentifys = OnlineImageIdentifyInfo.objects.all()
        singleImageIdentifyIdInt = int(singleImageIdentifyId)
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.id == int(singleImageIdentifyId):
                flyBackImagePath = singleImageIdentify.imageOriginPath
                break
        transBack(flyBackImagePath)
    context = identifyHtmlImages(userId, singleImageIdentifyIdInt, isNext)
    return render(request, 'identifyOnlineResult.html', context)

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
    context = identifyHtmlImages(resultId, None, None)
    return render(request, 'identifyOnlineResult.html', context)

def preprocessResult(request,resultId):
    context = preprocessHtmlImages(resultId,None,None)
    return render(request, 'preprocessOnlineResult.html', context)