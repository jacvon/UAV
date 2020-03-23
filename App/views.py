from django.http import HttpResponse
from django.shortcuts import render

from ModelToSQL.settings import BASE_DIR
from App.models import UserModel
#导入识别模块
from App.detect_project.predict_my import func_predict


def image_field(request):
    if request.method == "GET":
        return render(request, 'image_field.html')
    elif request.method == "POST":

        username = request.POST.get("username")

        icons = request.FILES.getlist("icon")

        for icon in icons:
            user = UserModel()
            user.u_name = username
            user.u_icon = icon
            user.save()
#            destination = open(BASE_DIR + '/static/upload/' + icon.name, 'wb+')
#            for part in icon.chunks():
#                destination.write(part)
#                destination.close()
        return HttpResponse("上传成功")


def mine(request):
    #图片分类，并将分类标签存入数据库
    users = UserModel.objects.all()
    for user in users:
        fname = BASE_DIR+"/static/upload/"+user.u_icon.url
        my_predict = func_predict(str(fname))
        user.u_predict = my_predict
        user.save()
        print("my_predict:", my_predict)
    #下面按理应该是取的最后一张图片
    data = {
            "username": user.u_name,
            "icon_url": "/static/upload/"+user.u_icon.url
        }

    return render(request, 'mine.html', context=data)
