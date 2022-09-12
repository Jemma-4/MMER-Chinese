from django.db import models


# Create your models here.
class Video(models.Model):
    video_md5 = models.CharField(primary_key=True, verbose_name="主键，视频md5值", max_length=32)
    video_path = models.CharField(max_length=200, verbose_name="视频文件名")

    class Meta:
        db_table = 'video'

