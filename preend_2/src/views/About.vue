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
            <line-chart-voice ref="line_chart_2"/>
            <div class="boxfoot"></div>
          </div>
        </li>
        <li>
          <div class="bar">
            <div class="barbox">
              <div
                v-for="item in mer_typelist"
                :key="item.type"
                class="mer_block"
              >
                <div class="mer_label" :style="{ background: item.color }" />
                <div class="mer_title">{{ item.type }}</div>
              </div>
            </div>
          </div>
          <div class="video">
            <video preload controls v-on:timeupdate="updateChart">
              <source :src="video_url" />
            </video>
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
export default {
  name: "About",
  data() {
    return {
      videoMD5:'',
      video_url: '',
      current_time: 0,
      video_duration: 0,
      chartData: [],
      mer_typelist: this.$typelist,
      line_chart_point_limit: 15,
      chart_fresh_rate: 2,
    };
  },
  // 钩子函数
  mounted() {
    this.videoMD5 = this.$route.query.videoMD5
    this.video_url = baseurl + "playVideo/?videoid=" + this.$route.query.videoMD5
    console.log(this.videoMD5)
    this.getChartData();
  },
  components: {
    LineChartFace,
    LineChartVoice,
    BarChartWord,
    BarChartMulti,
  },
  methods: {
    updateChart(e) {
      var new_time = Math.floor(e.target.currentTime);
      var duration = Math.floor(e.target.duration);
      console.log("e.target.currentTime", e.target.currentTime);

      // 表情分析图以帧为单位刷新
      var frame_speed = this.chartData["data_face"]["frame_speed"]
      var new_time_face = Math.floor(e.target.currentTime*frame_speed);
      var duration_face = duration*frame_speed
      if(new_time_face!=duration_face&&new_time_face != 0){
        this.updateLineChart1(new_time_face, duration_face);
      }

      // 其余三张图表以秒为单位刷新
      if (new_time != duration && new_time % this.chart_fresh_rate == 0 && new_time != 0||Math.abs(this.current_time-new_time)>2) {
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
    getChartData() {
      get({
        url: baseurl + "getChartData/?videoid="+ this.videoMD5,
      }).then((res) => {
        this.chartData = res.data.data;
        console.log(this.chartData);
      });
    },
  },
};

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
.mainbox > ul {
  height: 100%;
}

.mainbox > ul > li {
  width: 30%;
  float: left;
  padding: 0 2px;
  height: 100%;
}

.mainbox > ul > li:nth-child(2) {
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
  height: 72%;
  padding-left: 1%;
  width: 99%;
  display: flex;
}

.video > video {
  width: 100%;
  align-self: center;
}
</style>