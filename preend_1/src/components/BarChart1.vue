<template>
  <div id="word">
    <div id="bar-chart-word"></div>
  </div>
</template>

<script>
export default {
  name: "BarChartWord",
  data() {
    return {};
  },
  methods: {
    drawChart(y_data) {
      let myBarChart1 = this.$echarts.init(
        document.getElementById("bar-chart-word")
      );

      let series = [];
      let x_data = [];
      for (var i = 0; i < this.$typelist.length; i++) {
        x_data.push(this.$typelist[i].type);

        let n = new Array(this.$typelist.length);
        n.fill(0, 0, this.$typelist.length); //填充数组
        n[i] = y_data[i];
        series.push({
          type: "bar",
          data: n,
          coordinateSystem: "polar",
          stack: "a",
          color: this.$typelist[i].color,
          emphasis: {
            focus: "series",
          },
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
      myBarChart1.setOption(option);
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
#word {
  height: 90%;
}
#bar-chart-word {
  /* margin-top:-15px; */
  width: 100%;
  height: 100%;
  /* background-color: aliceblue; */
}
</style>
