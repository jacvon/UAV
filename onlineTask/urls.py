from django.conf.urls import url

from onlineTask import views

urlpatterns = [
    url(r'^identifyResult/(?P<resultId>\w+)/', views.identifyResult, name='identifyResult'),
    url(r'^identifyConfirm/(?P<userId>\w+)/(?P<singleImageIdentifyId>\w+)/', views.identifyConfirm, name='identifyConfirm'),
]