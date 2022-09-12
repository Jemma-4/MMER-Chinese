import hashlib
import os
import uuid
import json
import numpy as np
import time
from myapp.utils.MyThread import MyThread
from myapp import opt
from myapp.models import Video

# 音频处理依赖
import moviepy.editor as mp
import scipy.io.wavfile as wavfile
import contextlib
import wave

def handle_uploaded_file(f):
    result = {}
    # 创建临时文件
    postfix = '.' + f.name.split('.')[1]
    tempname = str(uuid.uuid4())+postfix
    md5 = hashlib.md5()
    temp_path = opt.videoroot + '%s' % tempname
    with open(temp_path, 'wb+') as video:
        for chunk in f.chunks():
            video.write(chunk)
            md5.update(chunk)
    video.close()
    md5_val = md5.hexdigest()
    result['data'] = md5_val

    # 判断MD5，数据库查询该视频是否已经上传过
    if video_exist(md5_val):
        result['msg'] = 'video already exist'
        os.remove(temp_path)
    else:
        video_path = opt.videoroot + '%s' % (md5_val + postfix)
        os.rename(temp_path, video_path)
        Video.objects.create(video_md5=md5_val, video_path=video_path)
        result['msg'] = 'upload success'
        # 模拟上传后长时间处理过程
        new_thread = MyThread(target=process_video, args=(md5_val, ), name='thread %s' % md5_val )
        new_thread.start()
        # process_video(md5_val)

    return result


def video_exist(md5_val):
    video = Video.objects.filter(video_md5=md5_val)
    if len(video) != 0:
        return True
    else:
        return False


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    # 每次最多读取8Kb
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length  # 还有多少未读取
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:  # 没有数据了 退出
                break
            if remaining:
                remaining -= len(data)
            yield data


def get_video_path(md5_val):
    video = Video.objects.filter(video_md5=md5_val)
    return video[0].video_path


# 预留处理视频函数，目前制造假数据
def process_video(md5_val):
    json_file = md5_val + '.json'
    video_duration = 145
    frame_speed = 3
    time.sleep(5)
    print('here')

    # 4个表，8种情绪，随时长变化的数值目前假定145秒视频每秒有数值
    # 其中表情相关数据以帧为单位刷新，测试设定为一秒3帧
    data={}
    data_face = np.random.randint(1,100,size=(8,video_duration*frame_speed)).tolist()
    data_voice = np.random.randint(1,100,size=(8,video_duration)).tolist()
    data_word = np.random.randint(1,100,size=(8,video_duration)).tolist()
    data_multi = np.random.randint(1,100,size=(8,video_duration)).tolist()
    data["data_face"] = {
        "frame_speed":frame_speed,
        "data":data_face}
    data["data_voice"] = { "data":data_voice }
    data["data_word"] = { "data":data_word }
    data["data_multi"] = { "data":data_multi }
    
    json.dump(data, open(opt.videoroot + '%s' % json_file, 'w'))

# 从视频中分离音频
def detach_video_modal(md5_val):
    video_path = ''
    audio_path = ''
    root_path = './myapp/video'
    # if video_exist(md5_val):
        # video_path = get_video_path(md5_val)

    # 测试：绕过数据库
    if True:
        video_path = md5_val
        video_name = video_path.split('/')[-1].split(".")[0]
        audio_path = os.path.join(root_path,video_name + ".wav")
        clip_process = mp.VideoFileClip(video_path)
        clip_process.audio.write_audiofile(audio_path)
        audio_process(audio_path)

    else:
        print("视频资源数据库中不存在")

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
    elif sample_rate >32000:
        samplerate = 32000
    elif samplerate > 16000:
        samplerate = 16000
    else:
        samplerate = 8000

    if nchannels == 2:
        # 转换为单通道
        samplerate, data = wavfile.read(audio_path)
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
    if nchannels!=1:
        speech_target += "音频通道数有误--"
        return speech_target
    

    

    
if __name__ == '__main__':
    detach_video_modal('43a27a40fac909b35636d2e5a0df70ec')




