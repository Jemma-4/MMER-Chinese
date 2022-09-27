<template>
  <div class="block" style="height: 100%">
    <p class="title">ATMR心智系统</p>
    <div style="height: 70%">
      <el-steps
        :space="100"
        :active="curId"
        direction="vertical"
        finish-status="success"
        style="margin-left: 9%"
      >
        <el-step
          v-for="item in questionList"
          :key="item.id"
          :title="(item.id+1).toString()"
					:process-status="chosenList[curId]==1?'finish':'wait'"
        ></el-step>
      </el-steps>

      <div class="qusition-card">
        <div class="question">
          问题{{ questionList[curId].id + 1 }}：{{
            questionList[curId].question
          }}
        </div>
        <el-radio-group :v-model="answer" style="width:100%;">
          <el-radio
            v-for="option in questionList[curId].options"
            :key="option.id"
            :label="option.id"
            class="option"
            >{{ option.text }}</el-radio
          >
        </el-radio-group>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      curId: 15,
      answer: 0,
			answerList:[],
			chosenList:[1,1,1,1,1,1,0,0,0,0,0],
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
  height: 20%;
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
  padding: 19%;
  padding-top: 100px;
}

.question {
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

>>> .el-carousel__button {
  background-color: #99a9bf;
}

>>> .el-step__icon.is-text {
}

>>> .el-step__icon {
  width: 18px;
  height: 18px;
  font-size: 10px;
  border: 0px;
}

>>> .el-step__head.is-success .el-step__icon.is-text {
  background: #67c23a;
  width: 10px;
  height: 10px;
  font-size: 0px;
  border: 0px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.65), 0 0 12px rgba(0, 0, 0, 0.65);
}

>>> .el-step__title.is-success {
  color: white;
  font-size: 14px;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.45), 0 0 4px rgba(0, 0, 0, 0.45);
}

>>> .el-step__head.is-process .el-step__icon.is-text {
  background: rgba(100, 100, 100, 1);
  width: 10px;
  height: 10px;
  font-size: 0px;
  border: 0px;
  box-shadow: 0 0 8px rgba(255, 255, 255, 1), 0 0 8px rgba(255, 255, 255, 1);
}

>>> .el-step__title.is-process {
  color: white;
  font-size: 14px;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.45), 0 0 10px rgba(0, 0, 0, 0.45);
}

>>> .el-step__head.is-wait .el-step__icon.is-text {
  background: rgba(255, 255, 255, 1);
  width: 10px;
  height: 10px;
  font-size: 0px;
  border: 0px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.65), 0 0 12px rgba(0, 0, 0, 0.65);
}

>>> .el-step__title.is-wait {
  color: white;
  font-size: 14px;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.45), 0 0 4px rgba(0, 0, 0, 0.45);
}

>>> .el-step__line {
  background: white;
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.65), 0 0 16px rgba(0, 0, 0, 0.65);
  width: 1px;
}

>>> .el-step__main {
  padding-left: 2px !important;
}

>>> .el-step__line-inner{
	border:0px ;
}
</style>