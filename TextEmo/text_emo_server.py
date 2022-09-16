from flask import request, Flask
from flask_cors import CORS
from experiment import predict, data_preprocess
import os
import paddle
import json
# 导入paddlenlp相关的包
import paddlenlp as ppnlp

host = '127.0.0.1'
port = 2233
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
# 允许跨越访问
CORS(app)


# 加载模型和tokenizer
model = ppnlp.transformers.NeZhaForSequenceClassification.from_pretrained('nezha-large-wwm-chinese', num_classes=6)
tokenizer =  ppnlp.transformers.NeZhaTokenizer.from_pretrained('nezha-large-wwm-chinese')

# 加载训练好的模型参数
params_path = './checkpoint/model_state.pdparams'
if params_path and os.path.isfile(params_path):
    # 加载模型参数
    state_dict = paddle.load(params_path)
    model.set_dict(state_dict)
    print("Loaded parameters from %s" % params_path)
label_map = ["happy", "sad", "neutral", "fear", "angry", "surprise"]


# 文本情绪识别接口
# 输入为文本列表
@app.route("/textemo", methods=['POST'])
def recognition():
    data = request.form
    # print(data.get("text_list"))
    text_list = json.loads(data.get("text_list"))
    # print(text_list, type(text_list))
    if len(text_list) != 0:
        text_list = data_preprocess(text_list)
        result_emo = predict(text_list, model, tokenizer, label_map)
        return str({"ok":1, "emo":result_emo}).replace("'", '"')
    else:
        return str({"error": 1, "msg": "read text failed!"})


# debug最好是False，否则会占用两倍显存
if __name__ == "__main__":
    app.run(host=host, port=port, debug=False)