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


def handlePreprocess(user, newItem):
    singleImage = SingleImageInfo()
    singleImage.title = user.title
    singleImage.imageOriginPath = newItem
    singleImage.overDate = user.overDate

    #新建预测文件夹并存储预处理后的图片，后续该逻辑应放入预处理模块中
    file = newItem.split('/')[-1]
    #overDate = datetime.datetime.now().strftime("%Y%m%d/%H%M%S")
    #利用绝对路径来拷贝图片
    origin_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', newItem)
    preprocess_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR, 'static/upload', singleImage.title, user.overDate, 'preprocess')
    #在实际数据库中只存相对路径
    preprocess_relaFolder = '%s/%s/%s/' % (singleImage.title, user.overDate, 'preprocess')

    if not os.path.exists(preprocess_folder):
        os.makedirs(preprocess_folder)

    shutil.copy(origin_folder, preprocess_folder + file)
    singleImage.begin = datetime.datetime.now()
    singleImage.imagePreprocessPath = preprocess_relaFolder + file
    singleImage.save()

def storgeIdentify(singleImage):
    singleImage.is_identify = True
    file = singleImage.imagePreprocessPath.split('/')[-1]
    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    identify_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'identify')
    identify_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload',identify_relafolder)

    if not os.path.exists(identify_folder):
        os.makedirs(identify_folder)

    shutil.copy(preprocess_folder, identify_folder + file)
    singleImage.imageIdentifyPath = identify_relafolder + file
    singleImage.save()

def handleIdentify(user):
    singleImages = SingleImageInfo.objects.all()
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate and singleImage.is_identify == False:
            fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
            predict_result = func_predict(str(fname))
            if predict_result is 0 or 1:
                storgeIdentify(singleImage)

def storgeSplice(singleImage):
    singleImage.is_splice = True
    file = singleImage.imagePreprocessPath.split('/')[-1]

    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    splice_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'splice')
    splice_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', splice_relafolder)

    if not os.path.exists(splice_folder):
        os.makedirs(splice_folder)

    shutil.copy(preprocess_folder, splice_folder + file)
    singleImage.imageSplicePath = splice_relafolder + file
    singleImage.save()

def handleSplice(user):
    singleImages = SingleImageInfo.objects.all()
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate and singleImage.is_splice is False:
            fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
            predict_result = func_predict(str(fname))
            if predict_result is 0 or 1:
                storgeSplice(singleImage)


class PreprocessTaskAdmin(generic.BOAdmin):

    def load_identify_status(self):
        if self.identify_status == 'u':
            return '未识别'
        elif self.identify_status == 'd':
            return '已确认'
        elif self.identify_status == 'p':
            url = '/admin/preprocess/predictresult/%s/' % (self.id) # 跳转的超链接
            url_text = '请确认识别结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    load_identify_status.allow_tags = True
    load_identify_status.short_description = '识别任务状态'

    def load_splice_status(self):
        if self.splice_status == 'u':
            return '未拼接'
        elif self.splice_status == 'd':
            return '已完成'
        elif self.splice_status == 'p':
            return '正在拼接'
    load_splice_status.allow_tags = True
    load_splice_status.short_description = '拼接任务状态'

    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['begin', 'title', load_identify_status, load_splice_status]
    list_display_links = ['title']
    list_filter = ['identify_status','splice_status','title']
    search_fields = ['title']
    fields = (
        ('title'),('description'),('imageUploadPath')
    )
    form = UploadForm
    actions = ['image_todo']

    def get_queryset(self, request):
        return super(PreprocessTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    def image_todo(self,request,queryset):
        global title
        identifyNum = 0
        spliceNum = 0
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
                                #当预处理完成后，存入单个图像model预处理信息
                                if predict_result is 0 or 1:
                                    handlePreprocess(user,newItem)
                                identifyNum = identifyNum + 1
                                spliceNum = spliceNum + 1
                                if identifyNum%5 == 0:
                                    queryset.update(identify_status='p')
                                    print("起进程识别程序")
                                    handleIdentify(user)
                                if spliceNum%10 == 0:
                                    queryset.update(splice_status='p')
                                    print("起进程拼接程序")
                                    handleSplice(user)
                queryset.update(splice_status='d')
    image_todo.short_description = "开始处理"


admin.site.register(PreprocessTask, PreprocessTaskAdmin)
