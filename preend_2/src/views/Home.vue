<template>
  <div class="home">
    <router-view />
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  methods: {
  },
  computed: {
    defaultActive() {
      console.log('/' + this.$route.path.split('/').reverse()[0])
      return '/' + this.$route.path.split('/').reverse()[0];
        
    }
  }
};
</script>

<style scoped>
.menu{
  width: 200px;
  min-height: 714px;
  position:absolute;
}
</style>
