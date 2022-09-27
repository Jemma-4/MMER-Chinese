from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ..services.text import handle_uploaded_text, get_text_result, tag_text
# 接受上传的文本
@require_http_methods(["POST"])
def uploadText(request):
    response = {'ok': 0}
    try:
        text = request.POST.get('text')
        result = handle_uploaded_text(text)
        response['ok'] = 1
        response['result'] = result
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)


# 文本结果数据
@require_http_methods(["GET"])
def getTextResult(request):
    response = {'ok': 0}
    try:
        emotion_tag, text_list = get_text_result(str(request.GET.get('textID')))
        if emotion_tag is not None:
            response['ok'] = 1
            response['data'] = {
                'tag': emotion_tag,
                'text': [{'id': i + 1, 'text': text} for (i, text) in enumerate(text_list)]
            }
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)


# 标注文本
@require_http_methods(["GET"])
def tagText(request):
    response = {'ok': 0}
    try:
        tag_text(str(request.GET.get('textID')), str(request.GET.get('tag').split(',')))
        response['ok'] = 1
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)
