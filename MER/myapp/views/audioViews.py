import os
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from wsgiref.util import FileWrapper

from ..services.audio import handle_uploaded_audio, get_audio_path, tag_audio, get_audio_result
from ..services.video import process_video


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
    response = {'ok': 0}
    try:
        emotion_tag, rec_text = get_audio_result(str(request.GET.get('audioMD5')))
        if emotion_tag is not None:
            response['ok'] = 1
            response['data'] = {
                'tag': emotion_tag,
                'text': [{'id': i + 1, 'text': text} for (i, text) in enumerate(rec_text)]
            }
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)

# 播放音频 http://10.203.143.252:8000/api/playAudio/?audioMD5=fb05687e69f68a381fce8a76bca539e2
def playAudio(request):
    try:
        audio_file_path = get_audio_path(request.GET.get('audioMD5'))
        wrapper = FileWrapper(open(audio_file_path, 'rb'))

        response = HttpResponse(wrapper, content_type="audio/mpeg")
        response['Content-Length'] = os.path.getsize(audio_file_path)
        return response
    except:
        return HttpResponse()

# 标注音频
@require_http_methods(["GET"])
def tagAudio(request):
    response = {'ok': 0}
    try:
        tag_audio(str(request.GET.get('audioMD5')), str(request.GET.get('tag').split(',')))
        response['ok'] = 1
    except Exception as e:
        print(e)
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
