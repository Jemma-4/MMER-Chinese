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

      let series = {};
      let x_data = ["A", "T", "M", "R"];
      let color = ["#FFFF00", "#FFC0CB", "red", "#6495ED"];
      let n = [0, 0, 0, 0];
      for (var i = 0; i < x_data.length; i++) {
        let item = {
          value: y_data[x_data[i]],
          itemStyle: {
            color: color[i],
          },
        };
        n[i] = item;
      }

      series = {
        type: "bar",
        coordinateSystem: "polar",
        data: n,
        label: {
          show: true,
          position: "middle",
          formatter: "{b}: {c}",
        },
      };

      let option = {
        polar: {
          radius: [30, "80%"],
        },
        radiusAxis: {
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
        angleAxis: {
          type: "category",
          data: x_data,
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
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
