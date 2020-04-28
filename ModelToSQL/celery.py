from celery import Celery
from django.conf import settings
import os

# 为celery设置环境变量, 改为你项目的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelToSQL.settings')

# 创建应用
app = Celery('ModelToSQL')

# 配置应用
app.conf.update(
 # 本地Redis服务器
 BROKER_URL=settings.BROKER_URL,
)

app.autodiscover_tasks(settings.INSTALLED_APPS)