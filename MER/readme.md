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

创建数据库后，执行迁移脚本，在数据库中创建表
```
python manage.py makemigrations myapp
python manage.py migrate myapp
```

测试阶段，可以使用generFakeData请求,伪造数据

### 后端运行

```
python manage.py runserver
```

