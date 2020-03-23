from django.conf.urls import url

from App import views

urlpatterns = [

    url(r'^imagefield/', views.image_field, name='image_field'),

    url(r'^mine/', views.mine, name='mine'),
]
