from django.urls import path
# from . import views
from .views import videoViews, audioViews, textViews, ATMRViews

urlpatterns = [
    path('test/', videoViews.test, ),
    path('uploadVideo/', videoViews.uploadVideo,),
    path('playVideo/', videoViews.playVideo,),
    path('getChartData/', videoViews.getChartData,),
    path('generFakeData/', videoViews.generFakeData,),

    path('recognizeLongSpeech/', audioViews.recognizeLongSpeech,),
    path('uploadAudio/', audioViews.uploadAudio,),
    path('getAudioResult/', audioViews.getAudioResult,),
    path('playAudio/', audioViews.playAudio,),
    path('tagAudio/', audioViews.tagAudio,),

    path('uploadText/', textViews.uploadText,),
    path('getTextResult/', textViews.getTextResult,),
    path('tagText/', textViews.tagText,),

    path('getQuiz/', ATMRViews.getQuiz,),
    path('uploadQuizAnswer/', ATMRViews.uploadQuizAnswer,),
    path('getQuizAnswer/', ATMRViews.getQuizAnswer,),
]
