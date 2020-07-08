from django.conf.urls import url

from onlineTask import views

urlpatterns = [
    url(r'^identifyResult/(?P<resultId>\w+)/', views.identifyResult, name='identifyResult'),
    url(r'^preprocessResult/(?P<resultId>\w+)/', views.preprocessResult, name='preprocessResult'),
    url(r'^identifyConfirm/(?P<userId>\w+)/(?P<singleImageIdentifyId>\w+)/', views.identifyConfirm, name='identifyConfirm'),
    url(r'^preprocessConfirm/(?P<userId>\w+)/(?P<singlePreprocessImageId>\w+)/', views.preprocessConfirm, name='preprocessConfirm'),
]