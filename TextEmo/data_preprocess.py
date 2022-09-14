# 通过pandas读取并处理数据
import pandas as pd

label_list = ['happy', 'sad', 'neutral', 'fear', 'angry', 'surprise']

def label_process(label_str):
    for label in label_list:
        if label==label_str:
            return label_list.index(label)

train1 = pd.read_csv('./data/SMP2020/virus_train.csv')  # 疫情微博训练数据集
train2 = pd.read_csv('./data/SMP2020/usual_train.csv')  # 通用微博训练数据集
train = pd.concat([train1,train2], ignore_index=True)  # 拼接训练集

eval1 = pd.read_csv('./data/SMP2020/virus_eval_labeled.csv')  # 疫情微博验证数据集
eval2 = pd.read_csv('./data/SMP2020/usual_eval_labeled.csv')  # 通用微博验证数据集
eval = pd.concat([eval1,eval2], ignore_index=True)

test1 = pd.read_csv('./data/SMP2020/virus_test_labeled.csv')  # 疫情微博测试数据集
test2 = pd.read_csv('./data/SMP2020/usual_test_labeled.csv')  # 通用微博测试数据集
test = pd.concat([test1,test2], ignore_index=True)

total = pd.concat([train,eval,test], ignore_index=True)  # 构造总数据集便于统计分析

train.columns = ["id","text_a","label"]
eval.columns = ["id","text_a","label"]
test.columns = ["id","text_a","label"]
total.columns = ["id","text_a","label"]

train = train[['text_a', 'label']]
eval = eval[['text_a', 'label']]
test = test[['text_a', 'label']]
total = total[['text_a', 'label']]

# 消除空行
train = train.dropna(subset=['text_a'])
total = total.dropna(subset=['text_a'])
test = test.dropna(subset=['text_a'])
eval = eval.dropna(subset=['text_a'])

# 更换数据集中的标签
train['label'] = train['label'].apply(label_process)
eval['label'] = eval['label'].apply(label_process)
test['label'] = test['label'].apply(label_process)

# 对处理后的数据进行存储，格式统一为text_a,label
train.to_csv('./data/SMP2020/train.csv', sep='\t', index=False)
eval.to_csv('./data/SMP2020/valid.csv', sep='\t', index=False)
test.to_csv('./data/SMP2020/test.csv', sep='\t', index=False)
