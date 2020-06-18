"""ModelToSQL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
#from django.contrib import admin
import ModelToSQL.views
from ModelToSQL import settings, views
import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    url(r'^$', ModelToSQL.views.home),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^xadmin/offlineTask/', include(('offlineTask.urls',"offlineTask"), namespace='offlineTask')),
    url(r'^admin/', include(('offlineTask.urls',"offlineTask"), namespace='admin')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

xadmin.site.site_header = '无人机项目管理系统'
xadmin.site.site_title = '登录系统后台'
xadmin.site.index_title = '进度监控'
