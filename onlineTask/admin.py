# coding=utf-8
import os
from django.contrib import admin
from django.utils.html import format_html

from onlineTask.models import OnlineTask
from onlineTask.tasks import onlinemosiac_handle
from common import generic
from multiprocessing import freeze_support
from multiprocessing import Process, Event, Queue
import datetime

class OnlineTaskAdmin(generic.BOAdmin):

    def identify_status(self):
        if self.identify_status == 'u':
            return '未识别'
        elif self.identify_status == 'd':
            url = '/admin/onlineTask/identifyResult/%s/' % (self.id)  # 跳转的超链接
            url_text = '已确认'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
        elif self.identify_status == 'p':
            url = '/admin/onlineTask/identifyResult/%s/' % (self.id) # 跳转的超链接
            url_text = '请确认识别结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    identify_status.allow_tags = True
    identify_status.short_description = '识别状态'

    def preprocess_status(self):
        if self.preprocess_status == 'u':
            return '未处理'
        elif self.preprocess_status == 'd':
            url = '/admin/onlineTask/preprocessResult/%s/' % (self.id)  # 跳转的超链接
            url_text = '已完成'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
        elif self.preprocess_status == 'p':
            url = '/admin/onlineTask/preprocessResult/%s/' % (self.id)  # 跳转的超链接
            url_text = '正在预处理'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    preprocess_status.allow_tags = True
    preprocess_status.short_description = '预处理状态'

    def task_status(self):
        if self.task_status == 'u':
            return '未处理'
        elif self.task_status == 'd':
            return '已结束'
        elif self.task_status == 'p':
            return '正在进行'
    task_status.allow_tags = True
    task_status.short_description = '任务状态'

    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['begin', 'title', identify_status, preprocess_status, task_status]
    list_display_links = ['title']
    list_filter = ['title']

    fieldsets = [
        ('基础配置', {'fields':['title','description']}),
        ('可选配置', {'fields':['preprocessSet','isIdentifyPre']}),
        #('可选配置', {'fields':['preprocessSet','isIdentify','isIdentifyPre','isSplice','isSplicePre','isCompare','isComparePre']}),
    ]

    actions = ['image_todo']
    date_hierarchy = 'begin'

    def get_queryset(self, request):
        return super(OnlineTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    def image_todo(self,request,queryset):
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