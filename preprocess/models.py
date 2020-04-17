# coding=utf-8
import os
import datetime

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db import connection
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import ClearableFileInput, ModelForm, TextInput
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from idna import unicode
from pip._vendor.distlib._backport import shutil

from ModelToSQL.settings import TEMP_IMAGE_DIR, BASE_DIR
from common import const
from common import generic

IDENTIFY_STATUS_CHOICES = (
    ('u', '未识别'),
    ('d', '已确认'),
    ('p', '正在确认'),
)
SPLICE_STATUS_CHOICES = (
    ('u', '未拼接'),
    ('d', '已完成'),
    ('p', '正在拼接'),
)
PREPROCESS_STATUS_CHOICES = (
    ('u', '未处理'),
    ('d', '已完成'),
    ('p', '正在预处理'),
)
COMPARISON_STATUS_CHOICES = (
    ('u', '未比对'),
    ('d', '已完成'),
    ('p', '正在比对'),
)

def get_image_path(path,attribute):
    def upload_callback(instance, filename):
        overdate = datetime.datetime.now().strftime("%Y/%m/icons")
        return '%s/%s/%s/%s' % (overdate, path,unicode(slugify(getattr(instance, attribute))), filename)
    return upload_callback

class UploadImageList(TextInput):
    template_name = "upload_multi_img/upload_img_list.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

class ImageInput(ClearableFileInput):
    template_name = "upload_multi_img/image_multi_upload.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

class OfflineMapManage(models.Model):
    addTime = models.DateTimeField(_('创建时间'), blank=True, null=True)
    mapNickName = models.CharField(_('路线简称'),blank=False, max_length=100)
    mapDescription = models.TextField(_("描述"), blank=True, null=True)
    def __str__(self):
        return self.mapNickName

    def save(self, *args, **kwargs):
        self.addTime = datetime.datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('offlineMapManage')
        verbose_name_plural = _('路线管理')

class PreprocessTask(generic.BO):
    index_weight = 1
    title = models.ForeignKey(OfflineMapManage, verbose_name=u'路线选择',on_delete=models.CASCADE, help_text=u'请选择路线')
    #title = models.CharField(_("路线选择"), max_length=const.DB_CHAR_NAME_120)
    description = models.TextField(_("描述"), blank=True, null=True)
    identify_status = models.CharField(_("识别状态"), blank=True, null=True, max_length=const.DB_CHAR_CODE_6,choices=IDENTIFY_STATUS_CHOICES, default='u')
    splice_status = models.CharField(_("拼接状态"), blank=True, null=True, max_length=const.DB_CHAR_CODE_6,choices=SPLICE_STATUS_CHOICES, default='u')
    preprocess_status = models.CharField(_("预处理状态"), blank=True, null=True, max_length=const.DB_CHAR_CODE_6,choices=PREPROCESS_STATUS_CHOICES, default='u')
    comparison_status = models.CharField(_("比对状态"), blank=True, null=True, max_length=const.DB_CHAR_CODE_6,choices=COMPARISON_STATUS_CHOICES, default='u')
    #imageUploadPath = models.FileField(_('上传图片'),help_text=u'请上传原始图片')
    #imagePredictPath = models.ImageField(upload_to=get_image_path('predict','title'))
    #imageResultPath = models.ImageField(upload_to=get_image_path('result','title'))
    imagesOriginPathList = models.CharField('', max_length=10000)
    overDate = models.CharField('', max_length=45)

    def save(self, *args, **kwargs):
        # 阻止images字段的数据保存在数据库中，因为我们不需要
        self.images = ""
        model_images = []
        print(self.title)
        # 将暂存目录中的图片转存到正式目录
        for root, dirs, files in os.walk(TEMP_IMAGE_DIR):
            print('files:', files)
            for file in files:
                #if os.path.join(WEB_HOST_MEDIA_URL, file) in self.images_list:
                    overDate = datetime.datetime.now().strftime("%Y%m%d/%H%M%S")
                    self.overDate = overDate
                    origin_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR, 'static/upload', self.title.mapNickName, overDate, 'origin')
                    origin_relaFolder = '%s/%s/%s/' % (self.title.mapNickName, overDate, 'origin')
                    if not os.path.exists(origin_folder):
                        os.makedirs(origin_folder)
                    shutil.move(TEMP_IMAGE_DIR + file, origin_folder + file)
                    model_images.append(os.path.join(origin_relaFolder, file))

        # 清空暂存目录下所有图片
        shutil.rmtree(TEMP_IMAGE_DIR)
        os.mkdir(TEMP_IMAGE_DIR)
        # 将模型原来的图片URL换为存到正式目录后的URL
        if self.imagesOriginPathList is '':
            self.imagesOriginPathList = model_images
        # 必须调用父类的方法，否则数据不会保存
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = _('preprocesstask')
        verbose_name_plural = _('离线任务')

class UploadForm(ModelForm):
    imageUploadPath = forms.FileField(label="上传图片", widget=ImageInput, help_text="按住ctrl多选", required=False)
    imagesOriginPathList = forms.CharField(label='', widget=UploadImageList, help_text='', required=False)
    class Meta:
        model = PreprocessTask
        fields = ['imageUploadPath','imagesOriginPathList']

class SingleImageInfo(generic.BO):
    title = models.CharField(max_length=const.DB_CHAR_NAME_120)
    is_identify = models.BooleanField(default=False)
    is_confirm = models.BooleanField()
    is_show = models.BooleanField(default=False)
    is_splice = models.BooleanField(default=False)
    imageOriginPath = models.CharField('', max_length=10000)
    imagePreprocessPath = models.CharField('', max_length=10000)
    imageIdentifyPath = models.CharField('', max_length=10000)
    imageIdentifyResultPath = models.CharField('', max_length=10000)
    imageSplicePath = models.CharField('', max_length=10000)
    overDate = models.CharField('', max_length=45)

    class Meta:
        verbose_name = _('singleImageInfo')
        verbose_name_plural = _('图片信息')