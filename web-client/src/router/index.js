import {
  createRouter,
  createWebHashHistory,
} from "vue-router";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      redirect: "/dashboard",
    },
    {
      path: "/dashboard",
      component: () => import("@/layout/index.vue"),
      redirect: "/dashboard",
      children: [
        {
          path: "/dashboard",
          name: "home",
          component: () => import("@/views/dashboard.vue"),
        },
        // Under Construction
        {
          path: "/dev",
          name: "dev",
          component: () => import("@/views/dev.vue"),
        },
        {
          path: "/setup",
          name: "setup",
          component: () => import("@/views/experiment/setup.vue"),
        },
        {
          path: "/workFlow",
          name: "workFlow",
          component: () => import("@/views/experiment/workFlow.vue"),
        },
        {
          path: "/download",
          name: "download",
          component: () => import("@/views/experiment/download.vue"),
        },
        {
          path: "/result",
          name: "result",
          component: () => import("@/views/experiment/result/index.vue"),
        },
      ],
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/auth/login.vue"),
    },
    {
      path: "/siginUp",
      name: "siginUp",
      component: () => import("@/views/auth/siginUp.vue"),
    },
    {
      path: "/forgotPassword",
      name: "forgotPassword",
      component: () => import("@/views/auth/forgotPassword.vue"),
    },
    {
      path: "/secretKey",
      name: "secretKey",
      component: () => import("@/views/auth/secretKey.vue"),
    },
    {
      path: "/resetPassword",
      name: "resetPassword",
      component: () => import("@/views/auth/resetPassword.vue"),
    },
    {
      path: "/404",
      name: "404",
      component: () => import("@/views/404.vue"),
    },
    {
      path: "/:pathMatch(.*)",
      redirect: "/404",
    },
  ],
});

export default router;
