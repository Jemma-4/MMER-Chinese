from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, ),
    path('uploadVideo/', views.uploadVideo, ),
    path('playVideo/', views.playVideo,),
    path('getChartData/', views.getChartData,),
    path('generFakeData/', views.generFakeData,),
    path('RecognizeLongSpeech/', views.RecognizeLongSpeech)
]
