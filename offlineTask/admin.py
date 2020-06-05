# coding=utf-8
import os
from django.contrib import admin
from django.utils.html import format_html
from offlineTask.tasks import mosiac_handle
from common import generic
from offlineTask.models import OfflineTask, SingleImagePreprocessInfo, UploadForm, OfflineMapManage, \
    OfflinePreprocessSet
import datetime

class OfflineTaskAdmin(generic.BOAdmin):

    def identify_status(self):
        if self.identify_status == 'u':
            return '未识别'
        elif self.identify_status == 'd':
            return '已确认'
        elif self.identify_status == 'p':
            url = '/admin/offlineTask/identifyResult/%s/' % (self.id) # 跳转的超链接
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
            url = '/admin/offlineTask/spliceResult/%s/' % (self.id)  # 跳转的超链接
            url_text = '请确认拼接结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
    splice_status.allow_tags = True
    splice_status.short_description = '拼接状态'

    def preprocess_status(self):
        if self.preprocess_status == 'u':
            return '未处理'
        elif self.preprocess_status == 'd':
            return '已完成'
        elif self.preprocess_status == 'p':
            url = '/admin/offlineTask/preprocessResult/%s/' % (self.id)  # 跳转的超链接
            url_text = '请查看预处理结果'  # 显示的文本
            return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
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

    fieldsets = [
        ('基础配置', {'fields':['title','description','imageUploadPath']}),
        ('可选配置', {'fields':['preprocessSet','isIdentify','isIdentifyPre','isSplice','isSplicePre','isCompare','isComparePre','comparePath']}),
        #('可选配置', {'fields':['preprocessSet','isIdentify','isIdentifyPre','isSplice','isSplicePre','isCompare','isComparePre']}),
    ]

    form = UploadForm
    actions = ['image_todo']
    date_hierarchy = 'begin'

    def get_queryset(self, request):
        return super(OfflineTaskAdmin,self).get_queryset(request).filter(end__gt=datetime.date.today())

    def image_todo(self,request,queryset):
        global title, pathImage, pathCsv
        users = OfflineTask.objects.all()
        if queryset is not None:
            for title in queryset:
                for user in users:
                    if user.id == title.id:
                        print("start mosiac_handle Process")
                        #mosiac_handle.delay(user.folderOriginPath, user.overDate, user.title_id)
                        mosiac_handle(user.id)
                        #compare_handle.delay(user.id, pathImage, pathCsv)
                        print("Exitting mosiac_handle Process")
                queryset.update(splice_status='p',preprocess_status='p',identify_status = 'p')
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

class OfflinePreprocessSetAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['addTime','setNickName','is_brightness','is_dehaze','is_gamma','is_clahe']
    list_display_links = ['setNickName']
    fields = (
        ('setNickName'), ('is_brightness'),('is_dehaze'),('is_gamma'),('is_clahe')
    )
    date_hierarchy = 'addTime'

admin.site.register(OfflineTask, OfflineTaskAdmin)
admin.site.register(OfflineMapManage, OfflineMapManageAdmin)
admin.site.register(OfflinePreprocessSet, OfflinePreprocessSetAdmin)
