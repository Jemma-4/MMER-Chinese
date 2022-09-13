import re
import os
import mimetypes
import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from wsgiref.util import FileWrapper

from . import opt
from .services.audio import handle_uploaded_audio, get_audio_path
from .services.video import handle_uploaded_video, file_iterator, video_exist, get_video_path, process_video, detach_video_modal
 
# 测试接口
@require_http_methods(["GET"])
def test(request):
    response = {}
    try:
        # 保留视频分离音频的入口
        detach_video_modal('./myapp/video/test1.mp4')
        response['ok'] = 1
    except Exception as e:
        print(e)
        response['ok'] = 0
        response['error_num'] = 1
    return JsonResponse(response)

# 接受上传的视频
@require_http_methods(["POST"])
def uploadVideo(request):
    response = {'ok': 0}
    try:
        video = request.FILES['file']
        result = handle_uploaded_video(video)
        response['ok'] = 1
        response['result'] = result
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)

# 流式回传视频数据用于播放
def playVideo(request):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    # 这里规定存放视频文件夹
    md5_val = request.GET.get('videoid')

    path = ''
    if video_exist(md5_val):
        path = get_video_path(md5_val)
    else:
        return JsonResponse({'ok': 0, 'msg': 'video does not exist'})
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        response = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length),
                                         status=206, content_type=content_type)
        response['Content-Length'] = str(length)
        response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        response['Content-Length'] = str(size)
    response['Accept-Ranges'] = 'bytes'
    return response

# 回传图表数据
@require_http_methods(["GET"])
def getChartData(request):
    response = {}
    try:
        result_file_path = opt.videoroot + str(request.GET.get('videoid')) + '.json'
        result_data = json.load(open(result_file_path, 'r'))
        response['ok'] = 1
        response['data'] = result_data
    except Exception as e:
        print(e)
        response['ok'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)

# 接受上传的音频
@require_http_methods(["POST"])
def uploadAudio(request):
    response = {'ok': 0}
    try:
        audio = request.FILES['file']
        result = handle_uploaded_audio(audio)
        response['ok'] = 1
        response['result'] = result
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)

# 语音结果数据
@require_http_methods(["GET"])
def getAudioResult(request):
    response = {}
    try:
        result_file_path = opt.audioroot + str(request.GET.get('audioMD5')) + '.json'
        result_data = json.load(open(result_file_path, 'r'))
        response['ok'] = 1
        response['data'] = result_data
    except Exception as e:
        print(e)
        response['ok'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)

def playAudio(request):
    try:
        audio_file_path = get_audio_path(request.GET.get('audioMD5'))
        wrapper = FileWrapper(open(audio_file_path, 'rb'))

        response = HttpResponse(wrapper, content_type="audio/mpeg")
        response['Content-Length'] = os.path.getsize(audio_file_path)
        return response
    except:
        return HttpResponse()

@require_http_methods(["GET"])
def generFakeData(request):
    response = {}
    try:
        response['ok'] = 1
        process_video('43a27a40fac909b35636d2e5a0df70ec')

    except Exception as e:
        print(e)
        response['ok'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)

@require_http_methods(["GET"])
def recognizeLongSpeech(request):
    response = {}
    try:
        response['ok'] = 1
        process_video('43a27a40fac909b35636d2e5a0df70ec')

    except Exception as e:
        print(e)
        response['ok'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)