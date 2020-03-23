from django.conf.urls import url

from preprocess import views

urlpatterns = [
    url(r'^predictresult/(?P<resultId>\w+)/', views.image_predict, name='image_predict'),
    url(r'^predictconfirm/(?P<userId>\w+)/(?P<singleImageId>\w+)/', views.predict_confirm, name='predict_confirm'),
    url(r'upload_temp_image/', views.upload_temp_image, name="upload_temp_images")
]

