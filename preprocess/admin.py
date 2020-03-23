# coding=utf-8
import os

from django.contrib import admin
from django.utils.html import format_html
from numpy.core.defchararray import strip
from pip._vendor.distlib._backport import shutil

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR
from common import generic
from preprocess.models import PreprocessTask, UploadForm, SingleImageInfo
import datetime
from App.detect_project.predict_my import func_predict
from preprocess.views import image_predict


def storageSingleImage(user, predict_result, newItem):
    singleImage = SingleImageInfo()
    singleImage.title = user.title
    singleImage.predict_result = predict_result
    singleImage.is_predict = True
    singleImage.imageOriginPath = newItem

    #新建预测文件夹并存储预处理后的图片，后续该逻辑应放入预处理模块中
    file = newItem.split('/')[-1]
    overDate = datetime.datetime.now().strftime("%Y/%m/icons")
    #利用绝对路径来拷贝图片
    origin_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR, 'static/upload', overDate, 'origin', singleImage.title)
    predict_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR, 'static/upload', overDate, 'predict', singleImage.title)
    #在实际数据库中只存相对路径
    predict_relaFolder = '%s/%s/%s/' % (overDate, 'predict', singleImage.title)

    if not os.path.exists(predict_folder):
        os.makedirs(predict_folder)

    shutil.copy(origin_folder + file, predict_folder + file)
    singleImage.begin = datetime.datetime.now()
    singleImage.imagePredictPath = predict_relaFolder + file
    singleImage.save()


class PreprocessTaskAdmin(generic.BOAdmin):

    def load_status(self):
        if self.status == 'u':
            return '未执行'
        elif self.status == 'd':
            return '已完成'
        elif self.status == 'p':
            url = '/admin/preprocess/predictresult/%s/' % (self.id) # 跳转的超链接
            url_text = '识别中'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    load_status.allow_tags = True
    load_status.short_description = '状态'

    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['begin', 'title', load_status]
    list_display_links = ['title']
    list_filter = ['status']
    search_fields = ['title']
    fields = (
        ('title'),('description'),('imageUploadPath')
    )
    form = UploadForm
    actions = ['image_todo']

    def get_queryset(self, request):
        return super(PreprocessTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    #def save_model(self, request, obj, form, change):
        #if obj:
            #obj.user = request.user
        #super(PreprocessTaskAdmin,self).save_model(request,obj,form,change)

    def image_todo(self,request,queryset):
        global title
        users = PreprocessTask.objects.all()
        if queryset is not None:
            for title in queryset:
                for user in users:
                    if user.id == title.id:
                        model_image_list = user.imagesOriginPathList.split(",")
                        if model_image_list is not None:
                            for item in model_image_list:
                                newItem = item.replace("'", '').replace("[", '').replace("]",'').replace(' ','')
                                fname = BASE_DIR + "/static/upload/" + newItem
                                predict_result = func_predict(str(fname))
                                #存入单个图像model预处理信息
                                storageSingleImage(user,predict_result,newItem)

                queryset.update(status='p')
    image_todo.short_description = "开始识别"


admin.site.register(PreprocessTask, PreprocessTaskAdmin)
