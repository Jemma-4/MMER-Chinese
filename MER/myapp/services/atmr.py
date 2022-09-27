import json
from myapp.opt import atmrroot
from random import shuffle
from myapp.models import ATMRAnswer
from myapp.utils.IDGenerator import randomID

# 写个样例，后续可能随机题序？从题库抽题？
def get_quiz(rand = True):
    json_data = json.load(open(atmrroot + 'quiz_2.json', 'r', encoding='utf8'))
    if rand:
        shuffle(json_data)

    for (i, data) in enumerate(json_data):
        data['id'] = i
    return 1, json_data, randomID()


def upload_quiz_answer(quiz_id, answer_id, answer):
    print(answer)
    ATMRAnswer.objects.create(quiz_id=quiz_id, answer_id=answer_id, answer=answer)


def get_quiz_answer(answer_id):
    print(answer_id, type(answer_id))
    return json.loads(ATMRAnswer.objects.filter(answer_id=answer_id)[0].answer)
