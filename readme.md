## 项目整体说明

#### MER--项目后端

#### preend_1--项目前端一页版

#### preend_2--项目后端两页版，附带语音识别界面

#### PaddlePaddle-DeepSpeech--语音识别服务

> 项目源码：https://github.com/yeyupiaoling/PaddlePaddle-DeepSpeech
>
> 相关博客：https://blog.csdn.net/qq_33200967/article/details/102904306

+ 注意事项（补充相关博客）

  + 环境搭建

    ```shell
    // 该包版本问题，需要新版本覆盖
    python -m pip install markupsafe==2.0.1
    ```

  + 数据准备/训练模型/评估 **跳过**

  + 模型下载/三组参数

    解压至`PaddlePaddle-DeepSpeech/models`目录下

  + 导出模型
    ```
    python export_model.py --resume_model=./models/param/50.pdparams
    ```

  + web部署

    ```
    python infer_server.py
    //服务运行在5000端口
    //利用http://localhost:5000访问图形化界面
    ```

    具体接口在`infer_server.py`中说明

  + Tip

    模型处理的音频需要满足通道为1，频率在（8000，16000，24000，32000，48000）之中；

    在后端`MER`中提供音频规格化接口,原则上前端上传视频需要进行规格化处理后再传入语音识别接口。