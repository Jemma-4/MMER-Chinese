<template>
  <div id="voice">
    <div id="line-chart-voice"></div>
  </div>
</template>


<script>
export default {
  name: "LineChartVoice",
  data() {
    return {};
  },
  methods: {
    drawChart(x_data, y_data, new_time, line_chart_point_limit) {
      let myChart = this.$echarts.init(
        document.getElementById("line-chart-voice")
      );

      let series = [];
      for (var i = 0; i < this.$typelist.length; i++) {
        series.push({
          type: "line",
          data: y_data[i],
        });
      }

      let option = {
        grid: {
          top: "8%",
          left: "3%",
          right: "4%",
          bottom: "13%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: x_data,
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
        dataZoom: [
          {
            startValue: new_time - line_chart_point_limit + 1,
          },
          {
            type: "inside",
            bottom: "0px",
          },
        ],
        yAxis: {
          type: "value",
          axisLabel: this.$axisStyle.axisLabel,
        },
        series: series,
      };
      myChart.setOption(option);
    },
  },
};
</script>

<style scoped>
#voice {
  height: 90%;
}
#line-chart-voice {
  /* margin-top:-15px; */
  width: 100%;
  height: 100%;
  /* background-color: aliceblue; */
}
</style>