from flask import request, Flask, render_template
from flask_cors import CORS
from experiment import predict, data_preprocess

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
# 允许跨越访问
CORS(app)

# 文本情绪识别接口
# 输入为文本列表
@app.route("/text-emo", methods=['POST'])
def recognition():
    data = request.form
    text_list = data.get("text_list")
    if len(text_list) != 0:
        text_list = data_preprocess(text_list)
        result_emo = predict(text_list)
        return str({"ok":1,"emo":result_emo})
    else:
        return str({"error": 1, "msg": "read text failed!"})

if __name__ == "__main__":
    app.run()