# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

#这个没用，懒得删了
class Book(models.Model):
    b_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Book'


class UserModel(models.Model):
    u_name = models.CharField(max_length=16)
    # upload_to 相对路径，  相对于的是MEDIA_ROOT  媒体根目录
    u_icon = models.ImageField(upload_to='%Y/%m/%d/icons')
    u_predict = models.IntegerField(default=0)
