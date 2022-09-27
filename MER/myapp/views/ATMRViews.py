from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from myapp.services.atmr import get_quiz, upload_quiz_answer, get_quiz_answer

# 获取试题id，试题以及答题卡id  目前写死从单个文件quiz_1.json获取
@require_http_methods(["GET"])
def getQuiz(request):
    response = {'ok': 0}
    try:
        quiz_id, data, answer_id = get_quiz()
        response['ok'] = 1
        response['quiz_id'] = quiz_id
        response['answer_id'] = answer_id
        response['data'] = data
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)


# 接收答案
@require_http_methods(["POST"])
def uploadQuizAnswer(request):
    response = {'ok': 0}
    try:
        answer = request.POST.get('answer')
        quiz_id = request.POST.get('quiz_id')
        answer_id = request.POST.get('answer_id')
        upload_quiz_answer(quiz_id, answer_id, answer)
        response['ok'] = 1
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)


# 获取历史答案
@require_http_methods(["GET"])
def getQuizAnswer(request):
    response = {'ok': 0}
    try:
        answer_id = request.GET.get('answer_id')
        data = get_quiz_answer(answer_id)
        response['ok'] = 1
        response['data'] = data
    except Exception as e:
        print(e)
        response['msg'] = str(e)
    return JsonResponse(response)