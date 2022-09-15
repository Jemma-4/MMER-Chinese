# 音频处理依赖
import scipy.io.wavfile as wavfile
import numpy as np
import contextlib
import wave
import os
import time
from myapp.utils.MyThread import MyThread
from myapp.utils.extractMD5 import extractMD5
from myapp.models import Audio
from myapp import opt

def handle_uploaded_audio(f):
    result = {}
    # 创建临时文件
    md5_val, temp_path, postfix = extractMD5(f)

    result['data'] = md5_val

    # 判断MD5，数据库查询该视频是否已经上传过
    if audio_exist(md5_val):
        result['msg'] = 'audio already exist'
        os.remove(temp_path)
    else:
        video_path = opt.audioroot + '%s' % (md5_val + postfix)
        os.rename(temp_path, video_path)
        Audio.objects.create(audio_md5=md5_val, audio_path=video_path)
        result['msg'] = 'upload success'
        # 开线程防止阻塞
        new_thread = MyThread(target=process_audio_test, args=(md5_val,), name='thread %s' % md5_val)
        new_thread.start()
    return result


def process_audio_test(md5_val):
    # json_file = md5_val + '.json'
    time.sleep(5)

    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    audio.emotion_tag = '惆怅'
    audio.save()
    # data = {'result': '惆怅'}

    # json.dump(data, open(opt.audioroot + '%s' % json_file, 'w'))


def get_audio_path(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)
    return audio[0].audio_path


def get_audio_tag(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)
    return audio[0].emotion_tag


def audio_exist(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)
    if len(audio) != 0:
        return True
    else:
        return False


def tag_audio(md5_val, tag):
    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    audio.emotion_tag = tag
    audio.save()

# 音频格式统一为单声道，频率保持在(8000, 16000, 32000, 48000)中
def audio_process(audio_path):
    sample_rate = 0
    nchannels = 0
    with contextlib.closing(wave.open(audio_path, 'rb')) as wf:
        # 音频帧率
        sample_rate = wf.getframerate()
        # 音频通道数
        nchannels = wf.getnchannels()

    # framerate 帧速转换
    if sample_rate > 48000:
        samplerate = 48000
    elif sample_rate > 32000:
        samplerate = 32000
    elif sample_rate > 16000:
        samplerate = 16000
    else:
        samplerate = 8000

    _, data = wavfile.read(audio_path)
    if nchannels == 2:
        # 转换为单通道
        left = []
        right = []
        for item in data:
            left.append(item[0])
            right.append(item[1])
        wavfile.write(audio_path, samplerate, np.array(left))
    else:
        wavfile.write(audio_path, samplerate, np.array(data))


def audio_recognize(audio_path):
    speech_target = "--"
    sample_rate = 0
    nchannels = 0
    with contextlib.closing(wave.open(audio_path, 'rb')) as wf:
        # 音频帧率
        sample_rate = wf.getframerate()
        # 音频通道数
        nchannels = wf.getnchannels()
    if sample_rate not in (8000, 16000, 32000, 48000):
        speech_target += "音频频率有误--"
        return speech_target
    if nchannels != 1:
        speech_target += "音频通道数有误--"
        return speech_target
