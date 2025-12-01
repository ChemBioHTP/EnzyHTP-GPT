import router from "@/router";
import { getToken } from "@/utils/cache-token";
import Constants from "@/config";
import { message } from "ant-design-vue";
// 权限控制 路由跳转前
router.beforeEach((to, from, next) => {
  const token = getToken();
  // 放行页面: 登录页 注册页 忘记密码页 404页
  if (Constants.WhiteList.includes(to.path)) {
    next();
    return;
  }

  if (!token) {
    next("/login");
    return;
  } else {
    next();
    return;
  }

  // message.error("您没有权限访问此页面");
  // next("/404");
});
