<template>
  <div class="block" style="height: 100%">
    <div class="line"></div>
    <p class="title">ATMR心智系统</p>
    <div class="line-label">
      <div
        v-for="item in questionList"
        :key="item.id"
        class="line-icon"
        v-show="getShowById(item.id)"
        @click="curId=item.id"
      >
        <div
          :class="getClassByIdIcon(item.id)"
          style="float: left; margin-top: 1px"
        ></div>
        <div
          :class="getClassByIdTitle(item.id)"
          style="text-align: left; width: 10%"
        >
          {{ item.id + 1 }}
        </div>
      </div>
    </div>
    <div style="height: 70%">
      <div class="qusition-card" v-show="!isStart">
        <div>
          说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;说明介绍一下ATMR，balabalabala;
        </div>
        <el-button @click="onStart" class="start-button">开始答题</el-button>
      </div>

      <div class="qusition-card" v-show="isStart">
        <div class="question-title">
          问题{{ questionList[curId].id + 1 }}：{{
            questionList[curId].question
          }}
        </div>
        <audio controls style="display: none" id="audio">
          <!-- <source :src="questionList[curId].audioMD5" /> -->
          <source src="https://www.runoob.com/try/demo_source/horse.mp3" />
        </audio>
        <el-radio-group v-model="chosenList[curId]" style="width: 100%">
          <el-radio
            v-for="option in questionList[curId].options"
            :key="option.id"
            :label="option.id"
            @change="getFinished"
            class="option"
            >{{ option.text }}</el-radio
          >
        </el-radio-group>
        <el-button v-show="!isFinished" @click="onNext" class="button"
          >下一题</el-button
        >
        <el-button v-show="!isFinished" @click="onLast" class="button"
          >上一题</el-button
        >
        <el-button v-show="isFinished" @click="onSubmit" class="button"
          >提交</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isStart: false,
      curId: 0,
      chosenList: [],
      isFinished: false,
      questionList: [
        {
          id: 0,
          question: "请描述一下你最近的心情",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 1,
          question: "请描述一下你最近的心情",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 2,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 3,
          question: "会是什么颜色？",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 4,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 5,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 6,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 7,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 8,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 9,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 10,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 11,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 12,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 13,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 14,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 15,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 16,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 17,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 18,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 19,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 20,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 21,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 22,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 23,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 24,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 25,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 26,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
        {
          id: 27,
          question: "如果用一种颜色来形容的话",
          options: [
            {
              id: 1,
              text: "不符合",
            },
            {
              id: 2,
              text: "有点符合",
            },
            {
              id: 3,
              text: "一般符合",
            },
            {
              id: 4,
              text: "比较符合",
            },
            {
              id: 5,
              text: "非常符合",
            },
          ],
        },
      ],
    };
  },
  methods: {
    getClassByIdIcon(id) {
      if (this.curId == id) {
        return "is-process-icon";
      }

      if (this.chosenList[id] == 0 || this.chosenList[id] == null) {
        return "is-wait-icon";
      } else {
        return "is-success-icon";
      }
    },
    getClassByIdTitle(id) {
      if (this.curId == id) {
        return "is-process-title";
      }

      if (this.chosenList[id] == 0 || this.chosenList[id] == null) {
        return "is-wait-title";
      } else {
        return "is-success-title";
      }
    },
    getFinished() {
      let all = true;
      for (var i = 0; i < this.questionList.length; i++) {
        if (this.chosenList[i] == null || this.chosenList[i] == 0) {
          all = false;
        }
      }
      this.isFinished = all;
    },
    getShowById(id) {
      let min = this.curId - 5;
      let max = this.curId + 4;
      if (min < 0) {
        min = 0;
        max = 9;
      } else if (max >= this.questionList.length) {
        min = this.questionList.length - 10;
        max = this.questionList.length - 1;
      }
      if (id >= min && id <= max) {
        return true;
      } else {
        return false;
      }
    },
    onNext() {
      this.curId < this.questionList.length - 1 ? (this.curId += 1) : {};
      var music = document.getElementById("audio");
      music.play();
    },
    onLast() {
      this.curId > 0 ? (this.curId -= 1) : {};
      var music = document.getElementById("audio");
      music.play();
    },
    onStart() {
      this.isStart = true;
      var music = document.getElementById("audio");
      music.play();
    },
    onSubmit() {
      //提交数据
      //chosenList存放答案 index为题号 chosenList[index]为答案
      console.log(this.chosenList);
    },
  },
};
</script>

<style scoped>
.title {
  font-size: 36px;
  margin: 0px;
  line-height: 100%;
  height: 10%;
  line-height: 100px;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.45), 0 0 10px rgba(0, 0, 0, 0.45);
  font-weight: bold;
}

.qusition-card {
  background: rgba(255, 255, 255, 0.85);
  width: 60%;
  height: 70%;
  top: 20%;
  position: absolute;
  left: 20%;
  border-radius: 10px;
  padding: 18%;
  padding-top: 90px;
}

.question-title {
  font-size: 22px;
  margin: 0px;
  color: black;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.15), 0 0 10px rgba(0, 0, 0, 0.15);
  display: block;
  float: left;
  text-align: left;
  width: 100%;
}

.option {
  display: block;
  margin-top: 20px;
  width: 100%;
  float: left;
  text-align: left;
  font-size: 25px;
  color: black;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.15), 0 0 10px rgba(0, 0, 0, 0.15);
}

.is-success-icon {
  background: #67c23a;
  width: 12px;
  height: 12px;
  font-size: 0px;
  border: 0px;
  border-radius: 50%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.65), 0 0 12px rgba(0, 0, 0, 0.65);
}

.is-success-title {
  color: white;
  font-size: 14px;
  margin-left: 18px;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.45), 0 0 4px rgba(0, 0, 0, 0.45);
}

.is-process-icon {
  background: rgba(100, 100, 100, 1);
  width: 12px;
  height: 12px;
  font-size: 0px;
  border: 0px;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(255, 255, 255, 1), 0 0 8px rgba(255, 255, 255, 1);
}

.is-process-title {
  color: white;
  font-size: 14px;
  margin-left: 18px;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.45), 0 0 10px rgba(0, 0, 0, 0.45);
}

.is-wait-icon {
  background: rgba(255, 255, 255, 1);
  width: 12px;
  height: 12px;
  font-size: 0px;
  border: 0px;
  border-radius: 50%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.65), 0 0 12px rgba(0, 0, 0, 0.65);
}

.is-wait-title {
  color: white;
  font-size: 14px;
  margin-left: 18px;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.45), 0 0 4px rgba(0, 0, 0, 0.45);
}

.line {
  background: rgba(255, 255, 255, 0.45);
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.65), 0 0 16px rgba(0, 0, 0, 0.65);
  width: 2px;
  height: 68%;
  position: absolute;
  margin-left: 10%;
  margin-top: 10%;
}

.line-label {
  height: 70%;
  position: fixed;
  margin-left: 10%;
  margin-top: 5%;
}
.line-icon {
  margin-top: 29px;
  transform: translate(-5px);
}

.button {
  float: right;
  margin-top: 10px;
  margin-left: 18px;
}

.start-button {
  margin-top: 70px;
}

>>> .el-button {
  border: 0px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
}
</style>