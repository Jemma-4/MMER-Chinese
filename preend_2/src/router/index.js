import Vue from 'vue'
import VueRouter from 'vue-router'
import Upload from '../views/upload.vue'
import About from '../views/About.vue'
import AudioItem from '../views/AudioItem.vue'
import TextEmo from '../views/TextEmo.vue'
import ATMR from '../views/ATMR.vue'

Vue.use(VueRouter)
    // const originalPush = VueRouter.prototype.push
    // VueRouter.prototype.push = function push(location) {
    //   return originalPush.call(this, location).catch(err => err)
    // }

const routes = [{
        path: '/',
        name: 'Default',
        redirect: '/audio'
    },
    {
        path: '/upload',
        name: 'Upload',
        component: Upload
    },
    {
        path: '/home',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: About
    },
    {
        path: '/about',
        name: 'About',
        component: About
    }, //预览页
    {
        path: '/audio',
        name: 'TextEmo',
        component: TextEmo
    },
    {
        path: '/question',
        name: 'ATMR',
        component: ATMR
    }
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
})

export default router