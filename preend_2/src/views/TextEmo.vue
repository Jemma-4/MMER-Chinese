<template>
  <div class="block" style="height: 100%">
    <p class="title">语音情绪识别系统</p>

    <el-carousel
      :autoplay="false"
      trigger="click"
      height="520px"
      style="top: 2%; left: 15%; width: 70%; border-radius: 10px"
    >
      <el-carousel-item
        v-for="item in questionList"
        :key="item.id"
        style="background: rgba(255, 255, 255, 0.85)"
      >
        <audio-item :id="item.id" :question="item.question" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
import AudioItem from "./AudioItem.vue";
export default {
  components: {
    AudioItem,
  },
  data() {
    return {
      questionList: [
        {
          id: 1,
          question:
            "请描述一下你最近的心情，如果用一种颜色来形容的话，会是什么颜色？",
        },
        {
          id: 2,
          question:
            "请描述一下你最近的心情，如果用一种天气来形容的话，会是什么天气？",
        },
        {
          id: 3,
          question:
            "请描述一下你最近的心情，如果用一种颜色来形容的话，会是什么颜色？",
        },
      ],
    };
  },
  methods: {},
};
</script>

<style scoped>
.title {
  font-size: 36px;
  margin: 0px;
  line-height: 100%;
  height: 100px;
  line-height: 100px;
  color: white;
  text-shadow: 0 0 10px rgba(0,0,0,0.45), 0 0 10px rgba(0,0,0,0.45);
  font-weight: bold;
}

.question,
.result {
  font-size: 18px;
  color: #fff;
  margin: 0px;
  padding-bottom: 2%;
}

.recordBtns {
  padding-bottom: 2%;
}

>>> .el-carousel__button {
  background-color: #99a9bf;
}
</style>