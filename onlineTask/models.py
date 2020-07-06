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

class OnlineImageIdentifyInfo(models.Model):
    titleId = models.IntegerField(default=None)
    is_confirm = models.BooleanField()
    is_identify = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    progress = models.FloatField('', max_length=10, default='0')
    imagePreprocessPath = models.CharField('', max_length=1000)
    imageIdentifyPath = models.CharField('', max_length=1000)
    imageIdentifyResultPath = models.CharField('', max_length=1000)
    overDate = models.CharField('', max_length=45)

    class Meta:
        verbose_name = _('在线识别信息')
        verbose_name_plural = _('在线识别信息')

class OnlineTask(generic.BO):
    index_weight = 1
    title = models.CharField(verbose_name=u'任务标题', help_text=u'请输入标题',max_length=45)
    description = models.TextField(_("描述"), blank=True, null=True)
    overDate = models.CharField('', max_length=45)
    isIdentifyPre = models.BooleanField(_("识别是否预处理"),blank=True, null=False, max_length=const.DB_CHAR_CODE_2,default=True)
    identify_status = models.CharField(_("识别状态"), blank=True, null=True, max_length=const.DB_CHAR_CODE_6,choices=IDENTIFY_STATUS_CHOICES, default='u')

    def save(self, *args, **kwargs):
        overDate = datetime.datetime.now().strftime("%Y%m%d/%H%M%S")
        self.overDate = overDate
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('在线任务')
        verbose_name_plural = _('在线任务')