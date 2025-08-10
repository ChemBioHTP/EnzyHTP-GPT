import "./assets/css/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
import "@/router/permission";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import "@/assets/css/login.scss";
const app = createApp(App);
app.use(Antd);
app.use(router);
app.use(store)

app.mount("#app");
