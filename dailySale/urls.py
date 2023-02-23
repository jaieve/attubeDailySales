from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('baemin', views.baemin , name='baemin'),
    path('yogiyo', views.yogiyo , name='yogiyo'),
    path('coupang', views.coupang , name='coupang'),
    path('ttanggyeo', views.ttanggyeo , name='ttanggyeo'),
]