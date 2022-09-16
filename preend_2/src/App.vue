<template>
  <div id="app" :style="{ backgroundImage: 'url(' + bg_list[bg_index] + ')' }">
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      bg_index: 0,
      timer: null,
      bg_list: [
        "https://newids.seu.edu.cn/authserver/custom/images/main2.jpg",
        "https://newids.seu.edu.cn/authserver/custom/images/main3.jpg",
        "https://newids.seu.edu.cn/authserver/custom/images/main4.jpg",
        "https://newids.seu.edu.cn/authserver/custom/images/main5.jpg",
        "https://newids.seu.edu.cn/authserver/custom/images/main6.jpg",
        "https://newids.seu.edu.cn/authserver/custom/images/main7.jpg",
      ],
    };
  },
  methods: {
    randomBg: function () {
      this.bg_index = Math.floor(Math.random()*6)
    },
  },
  //调用
  mounted() {
    this.timer = setInterval(() => {
      setTimeout(this.randomBg);
    }, 5000);
  },

  //页面切除后解除定时
  beforeDestroy() {
    clearInterval(this.timer);
    this.timer = null;
  },
};
</script>

<style>
html,
body {
  margin: 0px;
  height: 100%;
  width: 100%;
  font-family: "微软雅黑";
  font-size: 29px;
}

* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

/*google滚动条样式*/

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-size: cover;
  color: #666;
  font-size: 0.1rem;
  height: 100%;
  width: 100%;
}
</style>
