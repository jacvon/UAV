from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class MyAppConfig(AppConfig):
    name = 'preprocess'
    verbose_name = _("图像离线处理")
