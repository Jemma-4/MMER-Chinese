import json
import requests
from myapp.utils.MyThread import MyThread
from myapp.utils.IDGenerator import randomID
from myapp.models import Text

text_emo_url = 'http://127.0.0.1:2233/textemo'

def handle_uploaded_text(text):
    result = {}
    textID = randomID()
    text_list = []
    for t in text.split('。'):
        if t != '':
            text_list.append(t)

    Text.objects.create(text_id=textID, text=text_list)
    result['msg'] = 'upload success'
    # 开线程防止阻塞
    new_thread = MyThread(target=process_text, args=(textID, text_list), name='thread %s' % textID)
    new_thread.start()

    result['data'] = textID
    return result


def process_text(textID, text):
    response = requests.post(text_emo_url, data={'text_list': json.dumps(text)})
    text_emo = response.json()['emo']
    txt = Text.objects.filter(text_id=textID)[0]
    print(text, text_emo)
    txt.emotion_tag = text_emo
    txt.save()


# def text_exist(text):
#     audio = Text.objects.filter(text=text)
#     if len(audio) != 0:
#         return True
#     else:
#         return False

def get_text_result(textID):
    text = Text.objects.filter(text_id=textID)[0]
    return json.loads(text.emotion_tag.replace("'", '"')), json.loads(text.text.replace("'", '"'))


def tag_text(textID, tag):
    text = Text.objects.filter(text_id=textID)[0]
    text.emotion_tag = tag
    text.save()