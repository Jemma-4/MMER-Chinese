import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { Upload, Button, Row, Select, Option, Message, Form, FormItem, Input, Loading, Carousel, CarouselItem, Card, Radio, RadioGroup, RadioButton, Steps, Step, Timeline, TimelineItem } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import * as echarts from 'echarts'

Vue.config.productionTip = false
Vue.use(Button)
Vue.use(Card)
Vue.use(Carousel)
Vue.use(CarouselItem)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Option)
Vue.use(Radio)
Vue.use(RadioButton)
Vue.use(RadioGroup)
Vue.use(Row)
Vue.use(Select)
Vue.use(Step)
Vue.use(Steps)
Vue.use(Timeline)
Vue.use(TimelineItem)
Vue.use(Upload)
Vue.use(Loading)

Vue.prototype.$echarts = echarts
Vue.prototype.$message = Message;

// 定义了情绪类别 和 相应的图表图例配色
Vue.prototype.$typelist = [{
    type: "开心",
    color: "#FFFF00",
}, {
    type: "惊讶",
    color: "#FFC0CB",
}, {
    type: "中性",
    color: "white",
}, {
    type: "疲惫",
    color: "#6495ED",
}, {
    type: "生气",
    color: "red",
}, {
    type: "厌恶",
    color: "#008000",
}, {
    type: "伤心",
    color: "gray",
}, {
    type: "害怕",
    color: "#A52A2A",
}]

// 统一图表x轴 y轴的配色
Vue.prototype.$axisStyle = {
    axisLabel: {
        show: true,
        textStyle: {
            color: "black",
        },
    },

    axisLine: {
        show: true, //是否显示轴线
        lineStyle: {
            color: "black", //刻度线的颜色
        },
    },
}
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')