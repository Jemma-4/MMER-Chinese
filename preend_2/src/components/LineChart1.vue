<template>
  <div id="face">
    <div id="line-chart-face"></div>
  </div>
</template>

<script>
export default {
  name: "LineChartFace",
  methods: {
    drawChart(x_data, y_data, new_time,line_chart_point_limit) {
      let myChart = this.$echarts.init(
        document.getElementById("line-chart-face")
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
          top:"8%",
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
        yAxis: {
          type: "value",
          axisLabel: this.$axisStyle.axisLabel,
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
        series: series,
      };
      myChart.setOption(option);
    },
  },
  computed: {
    defaultActive() {
      return "/" + this.$route.path.split("/").reverse()[0];
    },
  },
  mounted: function () {},
};
</script>

<style scoped>
#face {
  height: 90%;
}
#line-chart-face {
  /* margin-top:-15px; */
  width: 100%;
  height: 100%;
  /* background-color: aliceblue; */
}
</style>
