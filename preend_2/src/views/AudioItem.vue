<template>
  <div style="height: 100%">
    <div class="question-line">
      <p class="question">问题{{ id }} : {{ question }}</p>
      <div class="mode-line">
        <el-button @click="inputMode=0;processReady=false"
        :class="inputMode==0?'active':'default'">文本</el-button>
        <el-button @click="inputMode=1;processReady=false"
        :class="inputMode==1?'active':'default'">语音</el-button>
      </div>
    </div>

    <div v-show="inputMode==1" style="padding-top:1%;height: 25%;">
      <el-button @click="recordStatusChange" v-if="!this.recEnd">{{
        recBtnText
      }}</el-button>
      <el-button @click="destroyRecord" v-if="this.recorder">重置</el-button>
      <el-button @click="endRecord" v-if="this.recorder && !this.recEnd"
        >结束</el-button
      >
      <el-button @click="playRecord" v-if="this.recEnd">播放</el-button>
      <el-button @click="uploadAudioProcess" v-if="this.recEnd">上传</el-button>
      <el-upload
        :action="upload_url"
        :multiple="false"
        :file-list="fileList"
        :on-success="uploadAudioSuccess"
        :on-progress="uploadAudioProgress"
        ref="upload"
        style="display: inline-block; margin-left: 10px"
      >
        <el-button id="upload">上传已有文件</el-button>
      </el-upload>

      <h2 class="tip">录音时长：{{ duration }}s</h2>
      <div v-if="processReady">
        <audio controls>
          <source :src="audio_url" />
        </audio>
      </div>
    </div>

    <div v-show="inputMode==0" class="text-line">
      <el-input
        type="textarea"
        placeholder="请输入内容，用。分隔句子"
        v-model="textInput"
        maxlength="128"
        show-word-limit
        :autosize="{ minRows:4, maxRows: 4}"
        class="text-input"
      >
      </el-input>
      <el-button style="margin-top:4%;float:right;margin-right:10%;text-align:right;" @click="uploadTextProcess">上传</el-button>
    </div>

    <!-- 预测结果显示与标注模块 -->
    <div style="height: 60%">
      <div v-if="processReady" style="height: 100%;padding-left:5%;padding-right:5%;padding-top:1%;">
        <!-- <p class="result">初步判断：{{ resultData["result"] }}</p> -->
        <div v-for="item in textFromAudio" :key="item.id">
          <tag-item
            :id="item.id"
            :textToTag="item.text"
            :tagFromModel="getLabelFromText(emoFromText[item.id -1 ])"
            @tagFromUser="getTagFromUser"
            style="margin-bottom:4px;"
          />
        </div>

        <el-button type="primary" @click="onSubmit" style="margin-top:4px;">提交</el-button>
      </div>
      <div v-show="!recUpload" style="height: 100%; padding-top: 100px">
        提示信息：请您尽可能真实详尽地描述出您当前的感受。
      </div>

      <div
        v-if="recUpload"
        v-loading="!processReady"
        element-loading-text="模型处理中"
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.05)"
        style="height: 100%; padding-top: 100px"
      >
        提示信息：请您尽可能真实详尽地描述出您当前的感受。
      </div>
    </div>
    <!-- 标注数据	 -->
  </div>
</template>

<script>
import Recorder from "js-audio-recorder";
import { baseurl, get, post } from "../network/request.js";
import TagItem from "./TagItem.vue";

export default {
  components: {
    TagItem,
  },
  props: ["id", "question"],
  data() {
    return {
      duration: "0",
      recorder: null,
      recStart: false,
      recPause: false,
      recEnd: false,
      recUpload: false,
      recBtnText: "录音",
      processReady: true,
      inputMode: 0, //0：默认文字上传；1：语音上传
      textInput: "",
      audioMD5: "",
      textID: "",
      audio_url: "",
      upload_url: baseurl + "uploadAudio/",
      fileList: [],
      taglist: [
        { id: 1, tag: "开心" },
        { id: 2, tag: "惊讶" },
        { id: 3, tag: "中性" },
        { id: 4, tag: "生气" },
        { id: 5, tag: "伤心" },
        { id: 6, tag: "害怕" },
      ],
      textFromAudio: [],
      emoFromText: ["开心", "伤心"],
    };
  },
  methods: {
    // 是否支持录音
    canTalk() {
      return (
        window.location.protocol.indexOf("https") === 0 ||
        window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1"
      );
    },
    // 开始录音
    startRecord() {
      if (!this.canTalk()) {
        this.$message({
          type: "error",
          message:
            "由于浏览器安全策略, 非 HTTPS 或 非 localhost 访问, 录音功能不可用！",
          duration: 5000,
        });
        return;
      }
      if (!this.recorder) {
        this.recorder = new Recorder({
          // 以下是默认配置
          sampleBits: 16,
          sampleRate: 16000, // 浏览器默认的输入采样率,
          numChannels: 1,
        });
        this.recorder.onprocess = (duration) => {
          this.duration = duration.toFixed(1);
        };
        this.recorder
          .start()
          .then(() => {
            console.log("开始录音");
          })
          .catch((err) => {
            this.$alert("请插入麦克风!", "提示", {
              confirmButtonText: "确定",
              type: "warning",
              callback: (action) => {
                this.recorder = null;
              },
            });
            return;
          });
      }
    },
    // 暂停录音
    pauseRecord() {
      this.recorder && this.recorder.pause();
      console.log("暂停录音");
    },
    // 恢复录音
    resumeRecord() {
      this.recorder && this.recorder.resume();
      console.log("恢复录音");
    },
    // 录音状态改变
    recordStatusChange() {
      if (this.recStart) {
        if (this.recPause) {
          // 继续录音
          this.resumeRecord();
          this.recPause = false;
          this.recBtnText = "暂停";
        } else {
          //暂停
          this.pauseRecord();
          this.recPause = true;
          this.recBtnText = "继续";
        }
      } else {
        //开始
        this.startRecord();
        this.recStart = true;
        this.recBtnText = "暂停";
      }
    },
    // 结束录音
    endRecord() {
      this.recorder && this.recorder.stop();
      this.recEnd = true;
      console.log("结束录音");
    },
    // 取消录音
    destroyRecord() {
      this.recorder &&
        this.recorder.destroy().then(() => {
          this.duration = "0";
          this.recorder = null;
          this.recStart = false;
          this.recPause = false;
          this.recEnd = false;
          this.recBtnText = "录音";
          this.processReady = false;
          console.log("录音实例被销毁");
        });
    },
    // 播放录音
    playRecord() {
      this.recorder && this.recorder.play();
    },
    // 上传wav格式录音文件，此接口以后要调整到父级页面
    uploadAudioProcess() {
      this.recUpload = true;
      if (this.recorder) {
        this.uploadAudioProgress();
        let blob = this.recorder.getWAVBlob();
        let formData = new FormData();
        var that = this;
        formData.append("file", blob);

        post({
          url: baseurl + "uploadAudio/",
          data: formData,
        }).then((res) => {
          // console.log(res)
          if (res.data.ok != 0) {
            that.$message({
              title: "提示",
              message: "上传完毕，音频处理中...",
              duration: 0,
            });

            that.uploadAudioSuccess(res.data);
          }
          // console.log(that.audioMD5);
        });
      }
    },

    uploadAudioSuccess(response) {
      this.$refs.upload.clearFiles();
      var audioMD5 = response.result.data;
      this.audioMD5 = audioMD5;
      var that = this;

      var interval = setInterval(function () {
        get({
          url: baseurl + "getAudioResult/?audioMD5=" + audioMD5,
        }).then((res) => {
          if (res.data.ok != 0) {
            that.audio_url = baseurl + "playAudio/?audioMD5=" + audioMD5;
            var resultData = res.data.data;
            that.emoFromText = resultData.tag;
            that.textFromAudio = resultData.text;
            that.processReady = true;
            clearInterval(interval);

            that.$message.closeAll();
            that.$message({
              title: "成功",
              message: "处理完成",
              type: "success",
            });
          }
          // console.log(audioMD5);
        });
      }, 1000);
    },

    uploadAudioProgress() {
      this.processReady = false;
    },

    uploadTextProcess() {
      if (this.textInput) {
        let formData = new FormData();
        var that = this;
        formData.append("text", this.textInput); 

        post({
          url: baseurl + "uploadText/",
          data: formData,
        }).then((res) => {
          if (res.data.ok != 0) {
            that.$message({
              title: "提示",
              message: "上传完毕，文本处理中...",
              duration: 0,
            });

            that.uploadTextSuccess(res.data);
          }
        });
      }
    },

    // todo 收集前端的文本输入框数据 获取和提交音频一样的结果数据
    uploadTextSuccess(response) {
      var textID = response.result.data;
      this.textID = textID;
      var that = this;

      var interval = setInterval(function () {
        get({
          url: baseurl + "getTextResult/?textID=" + textID,
        }).then((res) => {
          if (res.data.ok != 0) {
            var resultData = res.data.data;
            that.emoFromText = resultData.tag;
            that.textFromAudio = resultData.text;
            that.processReady = true;
            clearInterval(interval);

            that.$message.closeAll();
            that.$message({
              title: "成功",
              message: "处理完成",
              type: "success",
            });
          }
          // console.log(audioMD5);
        });
      }, 1000);

      // 测试数据
      // this.textFromAudio = [
      //   { id: 0, text: "我觉得今天天气很好，阳光明媚。" },
      //   { id: 1, text: "就像我的心情一样舒畅。" },
      //   { id: 2, text: "我觉得今天的天气不是很好，阴沉沉的。" },
      //   {
      //     id: 3,
      //     text: "我觉得今天的天气不是很好，阴沉沉的，我觉得今天的天气不是很好，阴沉沉的。我觉得今天的天气不是很好，阴沉沉的，我觉得今天的天气不是很好，阴沉沉的。我觉得今天的天气不是很好，阴沉沉的，我觉得今天的天气不是很好，阴沉沉的。",
      //   },
      // ];
      // this.emoFromText = ["开心", "开心", "伤心", "伤心"];
      // this.processReady=true
      // console.log("haoye")
    },

    //提交音频标注 Todo 后续再根据需求补充题号id相关业务
    onSubmit() {
      if(this.inputMode == 1){
        get({
          url:
            baseurl +
            "tagAudio/?audioMD5=" +
            this.audioMD5 +
            "&tag=" + this.emoFromText
        }).then((res) => {
          if (res.data.ok != 0) {
            this.$message({
              title: "成功",
              message: "标注成功",
              type: "success",
            });
          }
        });
      }else if(this.inputMode == 0){
        get({
          url:
            baseurl +
            "tagText/?textID=" +
            this.textID +
            "&tag=" + this.emoFromText
        }).then((res) => {
          if (res.data.ok != 0) {
            this.$message({
              title: "成功",
              message: "标注成功",
              type: "success",
            });
          }
        });
      }
    },
    
    // 从返回的标签文本转换对应的数字标识 tag
    getLabelFromText(emo_text) {
      for (var i = 0; i < this.taglist.length; i++) {
        if (emo_text == this.taglist[i].tag) return this.taglist[i].id;
      }
    },
    getTagFromUser(val) {
      this.emoFromText[val.id - 1] = val.tag;
      console.log(this.emoFromText);
    },
  },
};
</script>

<style scoped>
.title {
  font-size: 32px;
  color: #fff;
  margin: 0px;
  padding-bottom: 4%;
  padding-top: 5%;
}

.question-line {
  height: 15%;
  padding-top:3%;
  padding-left:3%;
  margin-bottom:2%;
}
.mode-line{
  width: 30%;
  float: right;
  text-align: right;
  display: inline;
  padding-right:10%;
}

.text-line{
  height: 25%;
}

.text-input{
  width:68%;
  margin-top:16px;
  margin-left:3%;
  float: left;
}


.question {
  font-size: 18px;
  margin:0px;
  color: black;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.15), 0 0 10px rgba(0, 0, 0, 0.15);
  display: inline;
  width: 70%;
  float: left;
  text-align: left;
}
.result {
  font-size: 18px;
  margin: 24px;
  color: black;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.15), 0 0 10px rgba(0, 0, 0, 0.15);
}

.tip {
  margin: 20px;
}

.active{
  background:#ecf5ff !important;
  color:#409EFF;
}

.default{

}
>>> .el-button {
  border: 0px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
}

>>> .el-textarea__inner ,
>>> .el-textarea .el-input__count{
  background: rgba(0,0,0,0);
}
</style>