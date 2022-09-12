<template>
  <div id="multi">
    <div id="bar-chart-multi"></div>
  </div>
</template>

<script>
export default {
  name: "BarChartMulti",
  data() {
    return {};
  },
  methods: {
    drawChart(y_data) {
      let myChart = this.$echarts.init(
        document.getElementById("bar-chart-multi")
      );

      let series = [];
      let x_data = [];
      for (var i = 0; i < this.$typelist.length; i++) {
        x_data.push(this.$typelist[i].type);

        let n = new Array(this.$typelist.length);
        n.fill("", 0, this.$typelist.length); //填充数组
        n[i] = y_data[i];
        series.push({
          type: "bar",
          stack: "total",
          color: this.$typelist[i].color,
          label: {
            show: true,
          },
          data: n,
        });
      }

      let option = {
        grid: {
          top:"8%",
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "value",
          axisLabel: this.$axisStyle.axisLabel,
          axisLine: this.$axisStyle.axisLine,
        },
        yAxis: {
          type: "category",
          data: x_data,
          axisLabel: this.$axisStyle.axisLabel,
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
#multi {
  height: 90%;
}
#bar-chart-multi {
  width: 100%;
  height: 100%;
  /* background-color: aliceblue; */
}
</style>
