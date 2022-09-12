<template>
  <div id="app">
    <router-view />
  </div>
</template>

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
  background: #000000 url(./assets/images/bg.jpg) center top;
  background-size: cover;
  color: #666;
  font-size: 0.1rem;
  height: 100%;
  width: 100%;
}
</style>
