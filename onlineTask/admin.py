# coding=utf-8
import os
from django.contrib import admin
from django.utils.html import format_html

from onlineTask.models import OnlineTask
from onlineTask.tasks import onlinemosiac_handle
from common import generic
from offlineTask.models import OfflineTask, SingleImagePreprocessInfo, UploadForm, OfflineMapManage, \
    OfflinePreprocessSet
import datetime

class OnlineTaskAdmin(generic.BOAdmin):

    def identify_status(self):
        if self.identify_status == 'u':
            return '未识别'
        elif self.identify_status == 'd':
            return '已确认'
        elif self.identify_status == 'p':
            url = '/admin/onlineTask/identifyResult/%s/' % (self.id) # 跳转的超链接
            url_text = '请确认识别结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    identify_status.allow_tags = True
    identify_status.short_description = '识别状态'

    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['begin', 'title', identify_status]
    list_display_links = ['title']
    list_filter = ['title']

    fieldsets = [
        ('基础配置', {'fields':['title','description']}),
        ('可选配置', {'fields':['isIdentifyPre']}),
        #('可选配置', {'fields':['preprocessSet','isIdentify','isIdentifyPre','isSplice','isSplicePre','isCompare','isComparePre']}),
    ]

    form = UploadForm
    actions = ['image_todo']
    date_hierarchy = 'begin'

    def get_queryset(self, request):
        return super(OnlineTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    def image_todo(self,request,queryset):
        global title, pathImage, pathCsv
        users = OnlineTask.objects.all()
        if queryset is not None:
            for title in queryset:
                for user in users:
                    if user.id == title.id:
                        print("start onlinemosiac_handle Process")
                        #mosiac_handle.delay(user.folderOriginPath, user.overDate, user.title_id)
                        onlinemosiac_handle(user.id, queryset)
                        #compare_handle.delay(user.id, pathImage, pathCsv)
                        print("Exitting onlinemosiac_handle Process")
    image_todo.short_description = "开始处理"

admin.site.register(OnlineTask, OnlineTaskAdmin)