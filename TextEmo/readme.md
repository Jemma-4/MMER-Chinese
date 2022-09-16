#### TextEmo--文本情绪分类模型

+ **数据集**（SMP2020)

  数据集对应的分类标签：（喜悦、愤怒、恐惧、悲伤、中性和惊讶）

  Ekman (1992a) 提出的 6 种基本情绪类别（喜悦、愤怒、恐惧、悲伤、厌恶和惊讶）；

+ **模型**

  华为开源中文预训练模型NeZha(https://arxiv.org/abs/1909.00204)

+ **训练**

  运行`TextEmo/experiment.py--main(train())`

  模型参数保存在`TextEmo/checkpoint/model_state.pdparams`

+ **接口服务**

  运行`TextEmo/text_emo_server.py`