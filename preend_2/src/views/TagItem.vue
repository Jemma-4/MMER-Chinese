<template>
  <div>
    <div :class="'tag' + tagFromUser" v-show="!startLabel" style="height: 38px">
      {{this.getLabelFromId(tagFromUser)}}：{{ textToTag }}
    </div>
    <el-radio-group
      v-model="text_tagFromUser"
      v-show="startLabel"
      style="height: 38px"
    >
      <el-radio-button v-for="item in taglist" :key="item.id" :label="item.tag">
      </el-radio-button>
    </el-radio-group>
    <el-button v-show="!startLabel" @click="onStart">标注</el-button>
    <el-button v-show="startLabel" @click="onBack">确定</el-button>
  </div>
</template>

<script>
export default {
  components: {},
  props: ["id", "textToTag", "tagFromModel"],
  data() {
    return {
      tagFromUser: 0,
      startLabel: false,
      taglist: [
        { id: 1, tag: "开心" },
        { id: 2, tag: "惊讶" },
        { id: 3, tag: "中性" },
        { id: 4, tag: "生气" },
        { id: 5, tag: "伤心" },
        { id: 6, tag: "害怕" },
      ],
      text_tagFromUser: "开心",
    };
  },
  watch: {
    text_tagFromUser: function (newVal, oldVal) {
      console.log(newVal);
      this.tagFromUser = this.getLabelFromText(newVal); //newVal即是chartData
    },
  },

  mounted() {
    console.log("mounted钩子中接收", this.tagFromModel);
    this.tagFromUser = this.tagFromModel;
  },
  methods: {
    onStart() {
      this.startLabel = true;
    },
    onBack() {
      this.startLabel = false;
      let newTag = {
        id: this.id,
        tag: this.getLabelFromId(this.tagFromUser),
      };
      this.$emit("tagFromUser", newTag);
    },
    // 从返回的标签文本转换对应的数字标识 tag
    getLabelFromText(emo_text) {
      for (var i = 0; i < this.taglist.length; i++) {
        if (emo_text == this.taglist[i].tag) return this.taglist[i].id;
      }
    },
    getLabelFromId(emo_id) {
      for (var i = 0; i < this.taglist.length; i++) {
        if (emo_id == this.taglist[i].id) return this.taglist[i].tag;
      }
    },
  },
};
</script>

<style scoped>
.tag1 {
  color: pink;
  font-size: 20px;
  display: inline;
}
.tag2 {
  color: orange;
  font-size: 20px;
  display: inline;
}
.tag3 {
  color: black;
  font-size: 20px;
  display: inline;
}
.tag4 {
  color: red;
  font-size: 20px;
  display: inline;
}
.tag5 {
  color: blue;
  font-size: 20px;
  display: inline;
}
.tag6 {
  color: gray;
  font-size: 20px;
  display: inline;
}

</style>