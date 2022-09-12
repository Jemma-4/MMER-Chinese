<template>
  <div style="height: 100%">
    <div class="opt_box">
      <p class="title title_up" v-if="openCame">选择要上传的视频</p>
      <p class="title title_down" v-else>选择要上传的视频</p>
      <el-upload class="upload-demo" :action="upload_url" :multiple="false" :file-list="fileList"
        :on-success="uploadSuccess" :on-progress="uploadProcess">
        <el-button type="primary" id="upload">点击上传</el-button>
      </el-upload>
      <el-button size="small" @click="operCamera" :disabled="cameDis">
        <span v-if="!openCame">打开摄像头</span>
        <span v-else>关闭摄像头</span>
      </el-button>

      <el-button size="small" @click="record" :disabled="recordDis">
        <span v-if="button_status == 0">开始录像</span>
        <span v-else>停止录像</span>
      </el-button>
      <el-select v-model="selectedType" placeholder="请选择视频格式" :disabled="selectDis">
        <el-option v-for="(item, index) in supportedType" :key="index" :label="item" :value="index">
        </el-option>
      </el-select>
      <el-button size="small" @click="jump" v-if="processReady"> 查看分析 </el-button>
    </div>

    <div class="video_box" v-if="openCame">
      <video autoplay playsinline></video>
    </div>
    <div class="msg_box">
      <p>点击打开摄像头按钮后，浏览器会询问是否允许，请点击“允许”。</p>
      <div id="errorMsg"></div>
      <div id="tipMsg"></div>
    </div>
  </div>
</template>

<script>
import { baseurl, get } from "../network/request.js";
const constraints = (window.constraints = {
  audio: true,
  video: {
    width: 1280,
    height: 720,
  },
});
let recordedBlobs = [];
let mediaRecorder;
export default {
  data() {
    return {
      upload_url: baseurl + "uploadVideo/",
      fileList: [],
      resultlist: [],
      button_status: 0,
      supportedType: getSupportedMimeTypes(),
      selectedType: 0,
      openCame: false,
      cameDis: false,
      recordDis: true,
      selectDis: false,
      videoMD5: '',
      processReady: false,
    };
  },

  props: [],

  computed: {},

  methods: {
    /*上传的相关操作*/
    uploadProcess: function () {
      this.processReady = false;
    },

    uploadSuccess: function (response) {
      var videoMD5 = response.result.data;
      var that = this
      this.$message({
        title: '提示',
        message: '视频处理中...',
        duration:0
      });
      var interval = setInterval(function () {
        get({
          url: baseurl + "getChartData/?videoid=" + videoMD5,
        }).then((res) => {
          if (res.data.ok != 0) {
            that.videoMD5 = videoMD5;
            that.processReady = true;
            clearInterval(interval);

            that.$message.closeAll();
            that.$message({
              title: '成功',
              message: '处理完成',
              type: 'success'
            });
          }
          console.log(videoMD5);
        });
      }, 1000)

    },
    async operCamera() {
      if (this.openCame) {
        this.stopCamera();
      } else {
        await this.openCamera();
      }
    },
    async openCamera() {
      try {
        clearMsg();
        this.openCame = true;
        this.recordDis = false;
        showMsg("正在打开摄像头");
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        showMsg("获取到了stream");
        gotStream(stream);
      } catch (err) {
        showErrMsg(err, err);
      }
    },

    stopCamera() {
      showMsg("停止视频");
      const videoElem = document.querySelector("video");
      const stream = videoElem.srcObject;
      if (stream == null) {
        return;
      }
      const tracks = stream.getTracks();

      tracks.forEach(function (track) {
        track.stop();
      });
      videoElem.srcObject = null;
      window.stream = null;
      showMsg("停止完毕");
      this.openCame = false;
      this.recordDis = true;
      this.selectDis = false;
    },

    record() {
      if (this.button_status == 0) {
        recordedBlobs = [];
        const mimeType = this.supportedType[this.selectedType];
        const options = { mimeType };
        console.log(options);

        try {
          mediaRecorder = new MediaRecorder(window.stream, options);
        } catch (e) {
          showMsg(`创建MediaRecorder出错: ${JSON.stringify(e)}`);
          return;
        }

        showMsg("创建MediaRecorder", mediaRecorder, " -> options", options);
        this.button_status = 1;
        this.selectDis = true;
        this.cameDis = true;
        mediaRecorder.onstop = (event) => {
          showMsg("录制停止了: " + event);
          showMsg("录制的数据Blobs: " + recordedBlobs);
        };
        mediaRecorder.ondataavailable = handleDataAvailable;
        mediaRecorder.start();
        showMsg("录制开始 mediaRecorder: " + mediaRecorder);
      } else {
        mediaRecorder.stop();

        this.button_status = 0;
        this.selectDis = false;
        this.cameDis = false;
      }
    },
    jump() {
      this.$router.push({ name: "About", query: { videoMD5: this.videoMD5 } });
    },
  },
};

function showErrMsg(msg, error) {
  const errorElement = document.querySelector("#errorMsg");
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== "undefined") {
    console.error(error);
  }
}

function showMsg(msg) {
  const msgEle = document.querySelector("#tipMsg");
  msgEle.innerHTML += `<p>-> ${msg}</p>`;
  console.log(msg);
}

function clearMsg() {
  const msgEle = document.querySelector("#tipMsg");
  const errorElement = document.querySelector("#errorMsg");
  errorElement.innerHTML = ``;
  msgEle.innerHTML = `<p>开始初始化</p>`;
}

function gotStream(stream) {
  const videoEle = document.querySelector("video");
  const videoTracks = stream.getVideoTracks();
  showMsg(`正在使用的设备: ${videoTracks[0].label}`);
  window.stream = stream;
  videoEle.srcObject = stream;
}

function getSupportedMimeTypes() {
  const possibleTypes = [
    "video/webm;codecs=vp9,opus",
    "video/webm;codecs=vp8,opus",
    "video/webm;codecs=h264,opus",
  ];
  return possibleTypes.filter((mimeType) => {
    return MediaRecorder.isTypeSupported(mimeType);
  });
}

function handleDataAvailable(event) {
  console.log("handleDataAvailable", event.data);
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
    console.log(recordedBlobs);
    const blob = new Blob(recordedBlobs, { type: "video/webm" });
    console.log(blob);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "video_" + new Date().getTime() + ".webm";
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }, 100);
  }
}
</script>

<style scoped>
.title_down {
  padding-top: 12%;
}

.title_up {
  padding-top: 2%;
}

.title {
  font-size: 32px;
  color: #fff;
  margin: 0px;
  padding-bottom: 2%;
}

.msg_box {
  position: absolute;
  background: rgba(200, 200, 200, 0.2);
  width: 300px;
  height: 200px;
  top: 0px;
}

.opt_box {
  height: 30%;
}

.video_box {
  height: 70%;
  display: flex;
  color: white;
  z-index: -1;
  text-align: center;
  text-align: center;
  padding: 0 28%;
}

.video_box video {
  width: 100%;
  align-self: center;
}

.el-button {
  background: rgba(255, 255, 255, 0.25);
  border: 0px;
  height: 40px;
  border-radius: 8px;
  color: white;
  margin: 0px 20px;
  z-index: 100;
}

#upload {
  background: rgba(255, 255, 255, 0.25);
  border: 0px;
  height: 40px;
  width: 200px;
  border-radius: 8px;
  color: white;
  margin-bottom: 15%;
}

button.el-button.el-button--default.el-button--small.is-disabled {
  background: rgba(255, 255, 255, 0.25);
}

>>>.el-input--suffix .el-input__inner {
  background: rgba(255, 255, 255, 0.25);
  border: 0px;
  color: white;
}
</style>
