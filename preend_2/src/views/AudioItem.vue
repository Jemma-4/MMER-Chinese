<template>
  <div style="height: 100%">
    <div style="height: 30%">
      <p class="question">问题{{ id }} : {{ question }}</p>
      <el-button @click="recordStatusChange" v-if="!this.recEnd">{{
        recBtnText
      }}</el-button>
      <el-button @click="destroyRecord" v-if="this.recorder">重置</el-button>
      <el-button @click="endRecord" v-if="this.recorder && !this.recEnd"
        >结束</el-button
      >
      <el-button @click="playRecord" v-if="this.recEnd">播放</el-button>
      <el-button @click="uploadProcess" v-if="this.recEnd">上传</el-button>
      <el-upload
        :action="upload_url"
        :multiple="false"
        :file-list="fileList"
        :on-success="uploadSuccess"
        :on-progress="uploadProgress"
        ref="upload"
        style="display: inline-block; margin-left: 10px"
      >
        <el-button id="upload">上传已有文件</el-button>
      </el-upload>

      <h2 class="tip">录音时长：{{ duration }}s</h2>
      <div v-show="processReady">
        <audio controls>
          <source :src="audio_url" />
        </audio>
      </div>
    </div>

    <!-- 预测结果显示与标注模块 -->
    <div style="height: 70%">
      <div v-show="processReady" style="height: 100%">
        <!-- <p class="result">初步判断：{{ resultData["result"] }}</p> -->
        <div v-for="item in textFromAudio" :key="item.id">
          <tag-item
            :id="item.id"
            :textToTag="item.text"
            :tagFromModel="getLabelFromText(emoFromText[item.id - 1])"
            @tagFromUser="getTagFromUser"
          />
        </div>

        <el-button type="primary" @click="onSubmit">提交</el-button>
      </div>

      <div
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
      recBtnText: "录音",
      processReady: true,
      audioMD5: "",
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
      textFromAudio: [
        { id: 1, text: "我今天很开心" },
        { id: 2, text: "我今天很难过" },
        { id: 3, text: "我今天很生气" },
        { id: 4, text: "我今天很惊讶" },
        { id: 5, text: "我今天很害怕" },
      ],
      emoFromText: ["开心", "伤心", "生气", "惊讶", "害怕"],
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
    uploadProcess() {
      if (this.recorder) {
        this.uploadProgress();
        let blob = this.recorder.getWAVBlob();
        let formData = new FormData();
        var that = this;
        formData.append("file", blob); //后续需要改，传多个音频

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

            that.uploadSuccess(res.data);
          }
          // console.log(that.audioMD5);
        });
      }
    },

    uploadSuccess(response) {
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
            console.log(that.textFromAudio, that.emoFromText)
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
    uploadProgress() {
      this.processReady = false;
    },
    //提交音频标注 Todo 直接提交列表this.emoFromText+题号id
    onSubmit() {
      get({
        url:
          baseurl +
          "tagAudio/?audioMD5=" +
          this.audioMD5 +
          "&tag=" + ''
          
      }).then((res) => {
        if (res.data.ok != 0) {
          this.$message({
            title: "成功",
            message: "标注成功",
            type: "success",
          });
        }
      });
    },
    // 从返回的标签文本转换对应的数字标识 tag
    getLabelFromText(emo_text) {
      for (var i = 0; i < this.taglist.length; i++) {
        if (emo_text == this.taglist[i].tag) return this.taglist[i].id;
      }
    },
    getTagFromUser(val) {
      this.emoFromText[val.id-1]=val.tag
      console.log(this.emoFromText)
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

.question,
.result {
  font-size: 18px;
  margin: 24px;
}

.tip {
  margin: 20px;
}

>>> .el-button {
  border: 0px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 0px;
}
</style>