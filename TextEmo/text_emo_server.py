from flask import request, Flask, render_template
from flask_cors import CORS
from experiment import predict, data_preprocess
import os
import paddle

# 导入paddlenlp相关的包
import paddlenlp as ppnlp

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
label_map = ['happy', 'sad', 'neutral', 'fear', 'angry', 'surprise']


# 文本情绪识别接口
# 输入为文本列表
@app.route("/text-emo", methods=['POST'])
def recognition():
    data = request.form
    text_list = data.get("text_list")
    text_list = text_list.split("::")
    if len(text_list) != 0:
        text_list = data_preprocess(text_list)
        result_emo = predict(text_listl,model,tokenizer,label_map)
        return str({"ok":1,"emo":result_emo})
    else:
        return str({"error": 1, "msg": "read text failed!"})

if __name__ == "__main__":
    app.run(host="223.3.95.42",port="5000")