# 导入所需的第三方库
from doctest import Example
import math
from unittest import result
import numpy as np
import os
from functools import partial
from tqdm import tqdm
import paddle
import paddle.nn.functional as F
from paddle.utils.download import get_path_from_url

# 导入paddlenlp相关的包
import paddlenlp as ppnlp
from paddlenlp.data import JiebaTokenizer, Pad, Stack, Tuple, Vocab
from paddlenlp.datasets import MapDataset
from paddle.dataset.common import md5file

# 导入自定义的函数
from smp2020_dataloader import convert_example, create_dataloader,load_dataset
# 定义超参，loss，优化器等
from paddlenlp.transformers import LinearDecayWithWarmup

# 定义模型训练验证评估函数
@paddle.no_grad()
def evaluate(model, criterion, metric, data_loader):
    """
    Given a dataset, it evals model and computes the metric.

    Args:
        model(obj:`paddle.nn.Layer`): A model to classify texts.
        data_loader(obj:`paddle.io.DataLoader`): The dataset loader which generates batches.
        criterion(obj:`paddle.nn.Layer`): It can compute the loss.
        metric(obj:`paddle.metric.Metric`): The evaluation metric.
    """
    model.eval()
    metric.reset()
    losses = []
    for batch in data_loader:
        input_ids, token_type_ids, labels = batch
        logits = model(input_ids, token_type_ids)
        loss = criterion(logits, labels)
        losses.append(loss.numpy())
        correct = metric.compute(logits, labels)
        metric.update(correct)
        accu = metric.accumulate()
    print("eval loss: %.5f, accu: %.5f" % (np.mean(losses), accu))
    model.train()
    metric.reset()
    return accu  # 返回准确率

def train(args,
          model,
          tokenizer,
          train_data_loader,
          dev_data_loader,):
    save_dir = "../checkpoint"
    if not  os.path.exists(save_dir):
        os.makedirs(save_dir)

    weight_decay = args["weight_decay"]
    learning_rate = args["learning_rate"]
    num_training_steps = args["num_training_steps"]
    warmup_proportion = args["warmup_proportion"]

    lr_scheduler = LinearDecayWithWarmup(learning_rate, num_training_steps, warmup_proportion)
    # AdamW优化器
    optimizer = paddle.optimizer.AdamW(
        learning_rate=lr_scheduler,
        parameters=model.parameters(),
        weight_decay=weight_decay,
        apply_decay_param_fun=lambda x: x in [
            p.name for n, p in model.named_parameters()
            if not any(nd in n for nd in ["bias", "norm"])
        ])
    # 交叉熵损失函数
    criterion = paddle.nn.loss.CrossEntropyLoss()  
    # accuracy评价指标
    metric = paddle.metric.Accuracy()  

    pre_accu=0
    accu=0
    global_step = 0
    for epoch in range(1, args["epochs"] + 1):
        for step, batch in enumerate(train_data_loader, start=1):
            input_ids, segment_ids, labels = batch
            logits = model(input_ids, segment_ids)
            loss = criterion(logits, labels)
            probs = F.softmax(logits, axis=1)
            correct = metric.compute(probs, labels)
            metric.update(correct)
            acc = metric.accumulate()

            global_step += 1
            if global_step % 10 == 0 :
                print("global step %d, epoch: %d, batch: %d, loss: %.5f, acc: %.5f" % (global_step, epoch, step, loss, acc))
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.clear_grad()
        # 每轮结束对验证集进行评估
        accu = evaluate(model, criterion, metric, dev_data_loader)
        print(accu)
        if accu > pre_accu:
            # 保存较上一轮效果更优的模型参数
            save_param_path = os.path.join(save_dir, 'model_state.pdparams')  # 保存模型参数
            paddle.save(model.state_dict(), save_param_path)
            pre_accu=accu
    tokenizer.save_pretrained(save_dir)

def main():
    # 批处理大小，显存如若不足的话可以适当改小该值  
    batch_size = 8
    # 文本序列最大截断长度，需要根据文本具体长度进行确定，不超过512
    max_seq_length = 128

    # 使用中文预训练模型NeZha
    model = ppnlp.transformers.NeZhaForSequenceClassification.from_pretrained('nezha-large-wwm-chinese', num_classes=6)
    tokenizer =  ppnlp.transformers.NeZhaTokenizer.from_pretrained('nezha-large-wwm-chinese')

    # 加载训练、验证集和测试集
    train_ds, dev_ds, test_ds = load_dataset(splits=["train", "dev", "test"])

    # 将数据处理成模型可读入的数据格式
    trans_func = partial(
        convert_example,
        tokenizer=tokenizer,
        max_seq_length=max_seq_length)

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # input_ids
        Pad(axis=0, pad_val=tokenizer.pad_token_type_id),  # token_type_ids
        Stack()  # labels
    ): [data for data in fn(samples)]

    # 训练集迭代器
    train_data_loader = create_dataloader(
    train_ds,
    mode='train',
    batch_size=batch_size,
    batchify_fn=batchify_fn,
    trans_fn=trans_func)

    # 验证集迭代器
    dev_data_loader = create_dataloader(
        dev_ds,
        mode='dev',
        batch_size=batch_size,
        batchify_fn=batchify_fn,
        trans_fn=trans_func)

    # 测试集迭代器
    test_data_loader = create_dataloader(
        test_ds, 
        mode='test', 
        batch_size=batch_size, 
        batchify_fn=batchify_fn, 
        trans_fn=trans_func)

    # 定义模型超参数
    args = { }
    # 定义训练过程中的最大学习率
    args["learning_rate"] = 2e-5
    # 训练轮次
    args["epochs"] = 3
    # 学习率预热比例
    args["warmup_proportion"] = 0.1
    # 权重衰减系数，类似模型正则项策略，避免模型过拟合
    args["weight_decay"] = 0.01
    args["num_training_steps"] = len(train_data_loader) * args["epochs"]

    # 模型训练 todo
    # train(args,model,tokenizer,train_data_loader,dev_data_loader)

    # 测试模型 todo
    # 交叉熵损失函数
    criterion = paddle.nn.loss.CrossEntropyLoss()  
    # accuracy评价指标
    metric = paddle.metric.Accuracy()  
    test(model,criterion,metric,dev_data_loader,test_data_loader)

def test(model,criterion,metric,dev_data_loader,test_data_loader):
    params_path = './checkpoint/model_state.pdparams'
    if params_path and os.path.isfile(params_path):
        # 加载模型参数
        state_dict = paddle.load(params_path)
        model.set_dict(state_dict)
        print("Loaded parameters from %s" % params_path)
    # 测试最优模型参数在验证集上的分数
    evaluate(model, criterion, metric, dev_data_loader)

    # 对测试集进行评估
    evaluate(model, criterion, metric, test_data_loader)

def predict(text_emo):

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
    batch_size = 1
    label_map = ['happy', 'sad', 'neutral', 'fear', 'angry', 'surprise']

    # 分词 + 向量化
    examples = []
    for text in text_emo:
        input_ids, segment_ids = convert_example(
            text,
            tokenizer,
            max_seq_length=128,
            is_test=True)
        examples.append((input_ids, segment_ids))
    
    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # input id
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # segment id
    ): fn(samples)

    # Seperates data into some batches.
    batches = []
    one_batch = []
    for example in examples:
        one_batch.append(example)
        if len(one_batch) == batch_size:
            batches.append(one_batch)
            one_batch = []
    if one_batch:
        # The last batch whose size is less than the config batch_size setting.
        batches.append(one_batch)

    results = []
    model.eval()
    for batch in batches:
        input_ids, segment_ids = batchify_fn(batch)
        input_ids = paddle.to_tensor(input_ids)
        segment_ids = paddle.to_tensor(segment_ids)
        logits = model(input_ids, segment_ids)
        probs = F.softmax(logits, axis=1)
        idx = paddle.argmax(probs, axis=1).numpy()
        idx = idx.tolist()
        labels = [label_map[i] for i in idx]
        results.extend(labels)
    return results

# 用于构造适合模型的输入
def data_preprocess(text_list):
    result = []
    for text in text_list:
        text_item = {}
        text_item["text_a"] = text
        result.append(text_item)
    return result

if __name__== "__main__" :
    paddle.device.set_device('gpu:0')

    # 前端识别到的文本列表
    # 定义要进行预测的样本数据
    test_text = [
        # angry
        '更年期的女boss真的让人受不了，烦躁',
        # fear
        '尼玛吓死我了，人家剪个头发回来跟劳改犯一样短的可怕，后面什么鬼[黑线][黑线][黑线][白眼][白眼]',
        # sad
        '一个人真无聊，美食都没味了，你要在就好了…唉………',
        # neutral
        "这个村的年轻人大多数都出外打工。",
        # happy
        "谢谢honey们帮我庆祝生日！！！谢谢你们的祝福，谢谢身边的所有人！爱你们",
        # surprise
        "我竟然才知道我有一个富二代加官二代加红二代的朋友"
    ]
    print(predict(data_preprocess(test_text)))