from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MyAppConfig(AppConfig):
    name = 'onlineTask'
    verbose_name = _("图像在线处理")