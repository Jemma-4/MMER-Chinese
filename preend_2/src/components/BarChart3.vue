<template>
  <div id="report">
    <div id="bar-chart-report"></div>
  </div>
</template>

<script>
export default {
  name: "BarChartReport",
  data() {
    return {};
  },
  methods: {
    drawChart(y_data) {
      let myChart = this.$echarts.init(
        document.getElementById("bar-chart-report")
      );

      let series = [];
      let x_data = ['A','T','M','R'];
      let color = ["#FFFF00", "#FFC0CB", "red", "#6495ED"]
      for (var i = 0; i < x_data.length; i++) {
        let n = new Array(x_data.length);
        n.fill(0, 0, x_data.length); //填充数组
        console.log(x_data[i],  y_data[x_data[i]])
        n[i] = y_data[x_data[i]];
        series.push({
          type: "bar",
          stack: "total",
          coordinateSystem: "polar",
          color: color[i],
          emphasis: {
            focus: "series",
          },
          data: n,
        });
      }

      let option = {
        angleAxis: {
          type: "category",
          data: x_data,
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
        radiusAxis: {
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
        polar: {},
        series: series,
        legend: {
          show: false,
          data: x_data,
        },
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
#report {
  width: 100%;
  height: 100%;
}
#bar-chart-report {
  width: 100%;
  height: 100%;
  /* background-color: aliceblue; */

}
</style>
