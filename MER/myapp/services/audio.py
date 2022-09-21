# 音频处理依赖
import scipy.io.wavfile as wavfile
import numpy as np
import contextlib
import wave
import os
import requests
import json
from myapp.utils.MyThread import MyThread
from myapp.utils.extractMD5 import extractMD5
from myapp.models import Audio
from myapp import opt

audio_reco_url = 'http://127.0.0.1:5000/recognition'
text_emo_url = 'http://127.0.0.1:2233/textemo'


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
        audio_path = opt.audioroot + '%s' % (md5_val + postfix)
        os.rename(temp_path, audio_path)
        audio_format_confirm(audio_path)
        Audio.objects.create(audio_md5=md5_val, audio_path=audio_path)
        result['msg'] = 'upload success'
        # 开线程防止阻塞
        new_thread = MyThread(target=process_audio, args=(md5_val,), name='thread %s' % md5_val)
        new_thread.start()
    return result


def process_audio(md5_val):
    audio_path = get_audio_path(md5_val)
    response = requests.post(audio_reco_url, files={'audio': open(audio_path, 'rb')})
    audio_text = response.json()['result'].split('，')
    response = requests.post(text_emo_url, data={'text_list': json.dumps(audio_text)})
    text_emo = response.json()['emo']
    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    print(audio_text, text_emo)
    audio.emotion_tag = text_emo
    audio.rec_text = audio_text
    audio.save()


def get_audio_path(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    return audio.audio_path


def get_audio_result(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    return json.loads(audio.emotion_tag.replace("'", '"')), json.loads(audio.rec_text.replace("'", '"'))


def audio_exist(md5_val):
    audio = Audio.objects.filter(audio_md5=md5_val)
    if len(audio) != 0:
        return True
    else:
        return False


def tag_audio(md5_val, tag):
    print(md5_val, tag)
    audio = Audio.objects.filter(audio_md5=md5_val)[0]
    audio.emotion_tag = tag
    audio.save()

# 音频格式统一为单声道，频率保持在(8000, 16000, 32000, 48000)中
def audio_format_confirm(audio_path):
    sample_rate = 0
    nchannels = 0
    with contextlib.closing(wave.open(audio_path, 'rb')) as wf:
        # 音频帧率
        sample_rate = wf.getframerate()
        # 音频通道数
        nchannels = wf.getnchannels()

    # framerate 帧速转换
    if sample_rate in [48000, 32000, 16000, 8000]:
        samplerate = sample_rate
    elif sample_rate > 48000:
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
