from django.db import models


# Create your models here.
class Video(models.Model):
    video_md5 = models.CharField(primary_key=True, verbose_name="主键，视频md5值", max_length=32)
    video_path = models.CharField(max_length=200, verbose_name="视频文件名")

    class Meta:
        db_table = 'video'

class Audio(models.Model):
    audio_md5 = models.CharField(primary_key=True, verbose_name="主键，音频md5值", max_length=32)
    audio_path = models.CharField(max_length=200, verbose_name="音频文件名")
    emotion_tag = models.CharField(max_length=20, verbose_name="标签", null=True)
    rec_text = models.CharField(max_length=200, verbose_name="语音文本", null=True)
    class Meta:
        db_table = 'audio'
