### 环境
python 3.8.10


### 安装依赖
```
pip install -r requirements.txt
```

### 数据表设计

提前创建数据库 mmer  (Multiple Modalities Emotion Recognition)

| 字段名        | 意义      | 类型           |
|------------|---------|--------------|
| video_md5  | 视频的MD5值 | varchar(32)  |
| video_path | 视频地址    | varchar(200) |

| 字段名      | 意义         | 类型         |
| ----------- | ------------ | ------------ |
| audio_md5   | 音频的MD5值  | varchar(32)  |
| audio_path  | 音频地址     | varchar(200) |
| emotion_tag | 情绪标签     | varchar(20)  |
| rec_text    | 识别出的文字 | varchar(200) |

创建数据库后，执行迁移脚本，在数据库中创建表。<font style="color:red">只要model文件发生改变</font>的时候都运行以下命令，保证数据库正常运行。
```
python manage.py makemigrations myapp
python manage.py migrate myapp
```

测试阶段，可以使用generFakeData请求,伪造数据

### 后端运行
新建一个文件夹/MER/myapp/statics/，并在该文件夹下新建子文件夹temp audio video，用来存放数据，此文件夹不会被git上传

```
python manage.py runserver
```

### 其他
有部分变量命名规则和暑假开发video部分时，有差别（没时间核对），后续有空尽量统一命名规则。

