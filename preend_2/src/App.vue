<template>
  <div id="app">
    <img
      :src="bg_list[bg_index]"
      style="
        position: absolute;
        top: 0px;
        left: 0px;
        width: 100%;
        height: 100%;
        z-index: -1;
      "
    />
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      bg_index: 2,
      timer: null,
      bg_list: [
        require("./assets/images/0.jpg"),
        require("./assets/images/1.jpg"),
        require("./assets/images/2.jpg"),
        require("./assets/images/3.jpg"),
        require("./assets/images/4.jpg"),
        require("./assets/images/5.jpg"),
        require("./assets/images/6.jpg"),
        require("./assets/images/7.jpg"),
        require("./assets/images/8.jpg"),
        require("./assets/images/9.jpg"),
        require("./assets/images/10.jpg"),
        require("./assets/images/11.jpg"),
        require("./assets/images/12.jpg"),
        require("./assets/images/13.jpg"),
        require("./assets/images/14.jpg"),
        require("./assets/images/15.jpg"),
        require("./assets/images/16.jpg"),
        require("./assets/images/17.jpg"),
        require("./assets/images/18.jpg"),
        require("./assets/images/19.jpg"),
        require("./assets/images/20.jpg"),
        require("./assets/images/21.jpg"),
        require("./assets/images/22.jpg"),
        require("./assets/images/22.jpg"),
        require("./assets/images/23.jpg"),
        require("./assets/images/24.jpg"),
        require("./assets/images/25.jpg"),
        require("./assets/images/26.jpg"),
      ],
    };
  },
  methods: {
    randomBg: function () {
      this.bg_index = Math.floor(Math.random() * 27);
    },
  },
  //调用
  mounted() {
    this.timer = setInterval(() => {
      setTimeout(this.randomBg);
    }, 10000);
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
