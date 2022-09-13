from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, ),
    path('uploadVideo/', views.uploadVideo,),
    path('playVideo/', views.playVideo,),
    path('getChartData/', views.getChartData,),
    path('generFakeData/', views.generFakeData,),
    path('recognizeLongSpeech/', views.recognizeLongSpeech,),
    path('uploadAudio/', views.uploadAudio,),
    path('getAudioResult/', views.getAudioResult,),
    path('playAudio/', views.playAudio,)
]
