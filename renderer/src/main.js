import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import TDesign from 'tdesign-vue-next';

import '@/assets/css/global.css'
import 'tdesign-vue-next/es/style/index.css';

import vue3videoPlay from 'vue3-video-play' // 引入组件
import 'vue3-video-play/dist/style.css' // 引入css


const app = createApp(App);
app.use(TDesign);
app.use(vue3videoPlay)
app.use(router);
app.mount("#app");