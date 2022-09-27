from django.db import models


# Create your models here.
# 这里要改，后面修改所有文件相关字段
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


class Text(models.Model):
    text_id = models.CharField(primary_key=True, verbose_name="主键，文本id值", max_length=32)
    text = models.CharField(max_length=200, verbose_name="文本列表形式")
    emotion_tag = models.CharField(max_length=20, verbose_name="标签", null=True)

    class Meta:
        db_table = 'text'


# 备用方案，目前需求不需要将题存入使用数据库
# class ATMRQuestion(models.Model):
#     question_id = models.AutoField(primary_key=True, verbose_name="主键，问题id")
#     question_text = models.CharField(max_length=200, verbose_name="问题文本")
#     question_type = models.CharField(max_length=10, verbose_name="题型")
#     question_options = models.CharField(max_length=200, verbose_name="问题选项与得分")
#
#     class Meta:
#         db_table = 'atmr_question'


class ATMRAnswer(models.Model):
    answer_id = models.CharField(primary_key=True, verbose_name="主键，答题卡id值", max_length=32)
    quiz_id = models.IntegerField(verbose_name="使用的第几套问卷")
    answer = models.CharField(max_length=1000, verbose_name="答案列表")

    class Meta:
        db_table = 'atmr_answer'
