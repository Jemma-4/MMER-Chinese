<template>
  <div class="window">
    <div class="head">多模态情绪识别系统</div>
    <div class="mainbox">
      <ul>
        <li>
          <div class="boxall">
            <div class="alltitle">表情情绪分析图</div>
            <line-chart-face ref="line_chart_1" />
            <div class="boxfoot"></div>
          </div>
          <div class="boxall">
            <div class="alltitle">声音情绪分析图</div>
            <line-chart-voice ref="line_chart_2" />
            <div class="boxfoot"></div>
          </div>
        </li>
        <li>
          <div class="bar">
            <div class="barbox">
              <div v-for="item in mer_typelist" :key="item.type" class="mer_block">
                <div class="mer_label" :style="{ background: item.color }" />
                <div class="mer_title">{{ item.type }}</div>
              </div>
            </div>
          </div>

          
          <div class="video" v-if="openCame">
            <video class="camera" autoplay playsinline></video>
          </div>
          <div class="video" v-if="!openCame && video_freshed">
            <video preload controls v-on:timeupdate="updateChart">
              <source :src="video_url" />
            </video>
          </div>
          
          <div class="opt_box">
            <el-upload :action="upload_url" :multiple="false" :file-list="fileList" :on-success="uploadSuccess"
              :on-progress="uploadProcess" ref="upload">
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
          </div>
        </li>
        <li>
          <div class="boxall">
            <div class="alltitle">文字情绪分析图</div>
            <bar-chart-word ref="bar_chart_1" />
            <div class="boxfoot"></div>
          </div>
          <div class="boxall">
            <div class="alltitle">多模态情绪分析图</div>
            <bar-chart-multi ref="bar_chart_2" />
            <div class="boxfoot"></div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import LineChartFace from "../components/LineChart1";
import LineChartVoice from "../components/LineChart2";
import BarChartWord from "../components/BarChart1";
import BarChartMulti from "../components/BarChart2";
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
  name: "About",
  data() {
    return {
      upload_url: baseurl + "uploadVideo/",
      fileList: [],
      button_status: 0,
      supportedType: getSupportedMimeTypes(),
      selectedType: 0,
      openCame: false,
      cameDis: false,
      recordDis: true,
      selectDis: false,
      videoMD5: '',
      video_url: '',
      current_time: 0,
      video_duration: 0,
      chartData: [],
      mer_typelist: this.$typelist,
      line_chart_point_limit: 15,
      chart_fresh_rate: 2,
      video_freshed: true,
    };
  },
  // 钩子函数
  mounted() {
  },
  components: {
    LineChartFace,
    LineChartVoice,
    BarChartWord,
    BarChartMulti,
  },
  methods: {
    uploadProcess: function () {
      this.video_freshed = false;
    },

    uploadSuccess: function (response) {
      var videoMD5 = response.result.data;
      this.$refs.upload.clearFiles();
      var that = this
      this.$message({
        title: '提示',
        message: '视频处理中...',
        duration: 0
      });

      var interval = setInterval(function () {
        get({
          url: baseurl + "getChartData/?videoid=" + videoMD5,
        }).then((res) => {
          if (res.data.ok != 0) {
            that.chartData = res.data.data;
            that.videoMD5 = videoMD5;
            that.video_freshed = true;
            that.video_url = baseurl + "playVideo/?videoid=" + videoMD5;
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
        this.openCame = true;
        this.recordDis = false;
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        gotStream(stream);
      } catch (err) {
        return;
      }
    },
    stopCamera() {
      const videoElem = document.querySelector("video.camera");
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
          return;
        }
        this.button_status = 1;
        this.selectDis = true;
        this.cameDis = true;
        mediaRecorder.onstop = (event) => {
        };
        mediaRecorder.ondataavailable = handleDataAvailable;
        mediaRecorder.start();
      } else {
        mediaRecorder.stop();

        this.button_status = 0;
        this.selectDis = false;
        this.cameDis = false;
      }
    },
    updateChart(e) {
      var new_time = Math.floor(e.target.currentTime);
      var duration = Math.floor(e.target.duration);
      console.log("e.target.currentTime", e.target.currentTime);

      // 表情分析图以帧为单位刷新
      var frame_speed = this.chartData["data_face"]["frame_speed"]
      var new_time_face = Math.floor(e.target.currentTime * frame_speed);
      var duration_face = duration * frame_speed
      if (new_time_face != duration_face && new_time_face != 0) {
        this.updateLineChart1(new_time_face, duration_face);
      }

      // 其余三张图表以秒为单位刷新
      if (new_time != duration && new_time % this.chart_fresh_rate == 0 && new_time != 0 || Math.abs(this.current_time-new_time)>2) {
        this.updateBarChart1(new_time);
        this.updateBarChart2(new_time);
      }

      if (new_time != duration && new_time != 0) {
        this.updateLineChart2(new_time, duration)
      }

      this.video_duration = duration;
      this.current_time = new_time;
    },
    updateLineChart1(new_time, duration) {
      var start_time = 0
      var x_data = Array.from(
        Array(duration),
        (_val, index) => index + 1
      ).slice(start_time, new_time);

      var y_data = [];
      for (var i = 0; i < this.$typelist.length; i++) {
        y_data.push(this.chartData["data_face"]["data"][i].slice(start_time, new_time));
      }
      this.$refs.line_chart_1.drawChart(x_data, y_data,new_time,this.line_chart_point_limit);
    },
    updateLineChart2(new_time, duration) {
      var start_time = 0
      var x_data = Array.from(
        Array(duration),
        (_val, index) => index + 1
      ).slice(start_time, new_time);

      var y_data = [];
      for (var i = 0; i < this.$typelist.length; i++) {
        y_data.push(this.chartData["data_voice"]["data"][i].slice(start_time, new_time));
      }
      this.$refs.line_chart_2.drawChart(x_data, y_data,new_time,this.line_chart_point_limit);
    },
    updateBarChart1(new_time) {
      var y_data = [];
      // console.log("newtime", new_time);
      for (var i = 0; i < this.$typelist.length; i++) {
        y_data.push(this.chartData["data_word"]["data"][i][new_time]);
      }
      this.$refs.bar_chart_1.drawChart(y_data);
    },
    updateBarChart2(new_time) {
      var y_data = [];
      // console.log("newtime", new_time);
      for (var i = 0; i < this.$typelist.length; i++) {
        y_data.push(this.chartData["data_multi"]["data"][i][new_time]);
      }
      this.$refs.bar_chart_2.drawChart(y_data);
    },
    // getChartData() {
    //   get({
    //     url: baseurl + "getChartData/?videoid=" + this.videoMD5,
    //   }).then((res) => {
    //     this.chartData = res.data.data;
    //     this.video_freshed = true;
    //     console.log(this.chartData);
    //   });
    // },
  },
};

function gotStream(stream) {
  const videoEle = document.querySelector("video.camera");
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
/*目前获取数据是假的 */
</script>

<style scoped>
@charset "utf-8";

.window {
  height: 100%;
}

ul,
p {
  padding: 0;
  margin: 0;
}

.allchart {
  height: 210px;
}

.head {
  height: 8%;
  font-size: 22px;
  background: url(../assets/images/head_bg.png) no-repeat center center;
  background-size: 100% 100%;
  position: relative;
  z-index: 100;
  color: #fff;
  text-align: center;
  padding-top: 1%;
}

.mainbox {
  padding: 2px;
  height: 92%;
}

.mainbox>ul {
  height: 100%;
}

.mainbox>ul>li {
  width: 30%;
  float: left;
  padding: 0 2px;
  height: 100%;
}

.mainbox>ul>li:nth-child(2) {
  width: 40%;
  padding: 0;
}

.boxall {
  border: 1px solid rgba(25, 186, 139, 0.17);
  padding-top: -20px;
  background: rgba(255, 255, 255, 0.04) url(../assets/images/line.png);
  background-size: 100% auto;
  position: relative;
  margin-bottom: 1%;
  z-index: 10;
  height: 49%;
}

.boxall:before,
.boxall:after {
  position: absolute;
  width: 9px;
  height: 9px;
  content: "";
  border-top: 1px solid #02a6b5;
  top: 0;
}

.boxall:before,
.boxfoot:before {
  border-left: 1px solid #02a6b5;
  left: 0;
}

.boxall:after,
.boxfoot:after {
  border-right: 1px solid #02a6b5;
  right: 0;
}

.alltitle {
  text-align: center;
  font-family: 微软雅黑;
  font-size: 18px;
  color: whitesmoke;
  padding: 10px;
  width: 100%;
  height: 10%;
}

.boxfoot {
  position: absolute;
  bottom: 0;
  width: 100%;
  left: 0;
}

.boxfoot:before,
.boxfoot:after {
  position: absolute;
  width: 9px;
  height: 9px;
  content: "";
  border-bottom: 1px solid #02a6b5;
  bottom: 0;
}

.bar {
  background: rgba(101, 132, 226, 0.1);
  padding: 4px;
  width: 100%;
  height: 20%;
}

.barbox:before,
.barbox:after {
  position: absolute;
  width: 15px;
  height: 6px;
  content: "";
}

.barbox:before {
  border-left: 1px solid #02a6b5;
  left: 0;
  border-top: 1px solid #02a6b5;
}

.barbox:after {
  border-right: 1px solid #02a6b5;
  right: 0;
  bottom: 0;
  border-bottom: 1px solid #02a6b5;
}

.barbox {
  border: 1px solid rgba(25, 186, 139, 0.17);
  position: relative;
  height: 100%;
}

.mer_block {
  display: inline-block;
  height: 50%;
  width: 25%;
}

.mer_title {
  margin-top: 10px;
  font-size: 20px;
  font-family: 微软雅黑;
  color: white;
  height: 100%;
  margin-left: 15px;
  float: left;
}

.mer_label {
  margin-top: 13px;
  width: 20px;
  border-radius: 5px;
  height: 20px;
  display: inline-block;
  margin-left: 15px;
  float: left;
}

.video {
  height: 60%;
  padding-left: 1%;
  width: 99%;
  display: flex;
}

.video>video {
  width: 100%;
  align-self: center;
}

.opt_box {
  padding-top: 3%;
  height: 15%;
}

.el-button {
  background: rgba(255, 255, 255, 0.25);
  border: 0px;
  height: 40px;
  border-radius: 8px;
  color: white;
  margin: 0px 10px;
  z-index: 100;
}

#upload {
  background: rgba(255, 255, 255, 0.25);
  border: 0px;
  height: 40px;
  width: 200px;
  border-radius: 8px;
  color: white;
  margin-bottom: 5%;
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