from django.conf.urls import url

from offlineTask import views

urlpatterns = [
    url(r'^identifyResult/(?P<resultId>\w+)/', views.identifyResult, name='identifyResult'),
    url(r'^spliceResult/(?P<resultId>\w+)/', views.spliceResult, name='spliceResult'),
    url(r'^preprocessResult/(?P<resultId>\w+)/', views.preprocessResult, name='preprocessResult'),
    url(r'^identifyConfirm/(?P<userId>\w+)/(?P<singleImageIdentifyId>\w+)/', views.identifyConfirm, name='identifyConfirm'),
    url(r'^preprocessConfirm/(?P<userId>\w+)/(?P<singlePreprocessImageId>\w+)/', views.preprocessConfirm, name='preprocessConfirm'),
    url(r'^spliceConfirm/(?P<userId>\w+)/(?P<singleSpliceImageId>\w+)/', views.spliceConfirm, name='spliceConfirm'),
    url(r'upload_temp_image/', views.upload_temp_image, name="upload_temp_images")
]

