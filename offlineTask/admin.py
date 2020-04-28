# coding=utf-8
import os

from django.contrib import admin
from django.utils.html import format_html
from numpy.core.defchararray import strip
from pip._vendor.distlib._backport import shutil

from ModelToSQL.settings import BASE_DIR, TEMP_IMAGE_DIR
#from splice.app import handleSplice
#from identify.app import handleIdentify
from preprocess.app import handlePreprocess
from common import generic
from offlineTask.models import OfflineTask, SingleImageInfo, UploadForm, OfflineMapManage
import datetime
from identify.tasks import handleIdentify
from splice.tasks import handleSplice
from App.detect_project.predict_my import func_predict

class OfflineTaskAdmin(generic.BOAdmin):

    def identify_status(self):
        if self.identify_status == 'u':
            return '未识别'
        elif self.identify_status == 'd':
            return '已确认'
        elif self.identify_status == 'p':
            url = '/admin/offlineTask/predictresult/%s/' % (self.id) # 跳转的超链接
            url_text = '请确认识别结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    identify_status.allow_tags = True
    identify_status.short_description = '识别状态'

    def splice_status(self):
        if self.splice_status == 'u':
            return '未拼接'
        elif self.splice_status == 'd':
            return '已完成'
        elif self.splice_status == 'p':
            return '正在拼接'
    splice_status.allow_tags = True
    splice_status.short_description = '拼接状态'

    def preprocess_status(self):
        if self.preprocess_status == 'u':
            return '未处理'
        elif self.preprocess_status == 'd':
            return '已完成'
        elif self.preprocess_status == 'p':
            return '正在预处理'
    preprocess_status.allow_tags = True
    preprocess_status.short_description = '预处理状态'

    def comparison_status(self):
        if self.comparison_status == 'u':
            return '未比对'
        elif self.comparison_status == 'd':
            return '已完成'
        elif self.comparison_status == 'p':
            return '正在比对'
    comparison_status.allow_tags = True
    comparison_status.short_description = '比对状态'

    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['begin', 'title', identify_status, splice_status, preprocess_status, comparison_status]
    list_display_links = ['title']
    list_filter = ['title']
    #search_fields = ['title']
    fields = (
        ('title'),('description'),('imageUploadPath')
    )
    form = UploadForm
    actions = ['image_todo']
    date_hierarchy = 'begin'

    def get_queryset(self, request):
        return super(OfflineTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    def image_todo(self,request,queryset):
        global title
        identifyNum = 0
        spliceNum = 0
        users = OfflineTask.objects.all()
        if queryset is not None:
            for title in queryset:
                for user in users:
                    if user.id == title.id:
                        model_image_list = user.imagesOriginPathList.split(",")
                        if model_image_list is not None:
                            for item in model_image_list:
                                newItem = item.replace("'", '').replace("[", '').replace("]",'').replace(' ','')
                                queryset.update(preprocess_status='p')
                                handlePreprocess(user,newItem)
                                identifyNum = identifyNum + 1
                                spliceNum = spliceNum + 1
                                if identifyNum%10 == 0:
                                    queryset.update(identify_status='p')
                                    print("起进程识别程序")
                                    handleIdentify.delay(user)
                                if spliceNum%10 == 0:
                                    queryset.update(splice_status='p')
                                    print("起进程拼接程序")
                                    handleSplice.delay(user)
                queryset.update(splice_status='d',preprocess_status='d')
    image_todo.short_description = "开始处理"

class OfflineMapManageAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['addTime','mapNickName','mapDescription']
    list_display_links = ['mapNickName']
    fields = (
        ('mapNickName'), ('mapDescription')
    )
    date_hierarchy = 'addTime'

admin.site.register(OfflineTask, OfflineTaskAdmin)
admin.site.register(OfflineMapManage, OfflineMapManageAdmin)
