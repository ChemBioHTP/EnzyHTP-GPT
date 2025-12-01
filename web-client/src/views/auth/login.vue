<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Log in</div>
        <div class="tip">
          <span>New to MutexaGPT?</span>
          <span class="theme-color" @click="$router.push('/siginUp')">Sign up</span>
        </div>
      </div>

      <a-form :model="form" layout="vertical" hideRequiredMark autocomplete="off" @validate="handleValidate"
        @finish="onFinish" :rules="rules" :label-col="{ span: 24 }" class="mt60">
        <a-form-item label="Email address" name="email">
          <a-input v-model:value="form.email" :bordered="true" size="large" />
        </a-form-item>

        <a-form-item name="password">
          <template #label>
            <a-flex>
              <span>Password</span>
              <span class="forgot-password theme-color" @click="$router.push('/forgotPassword')">
                Forgot password?
              </span>
            </a-flex>
          </template>
          <a-input-password v-model:value="form.password" :bordered="true" size="large" />
        </a-form-item>

        <a-form-item name="remember" @click="form.remember = !form.remember">
          <a-flex align="center">
            <img src="@/assets/img/check.png" v-if="form.remember" class="icon" />
            <img src="@/assets/img/checked.png" class="icon" v-else />
            <span class="ml10">Remember ID</span>
          </a-flex>
          <!-- <a-checkbox v-model:checked="form.remember"></a-checkbox> -->
        </a-form-item>

        <a-form-item>
          <a-button block type="primary" size="large" :disabled="disabled" html-type="submit">
            <a-flex class="button-content" justify="space-between" align="center">
              <span>Continue</span>
              <LoadingOutlined v-if="loading" />
              <ArrowRightOutlined v-else />
            </a-flex>
          </a-button>
        </a-form-item>

        <a-form-item>
          <div class="gsi-material-button" @click="googleAuth">
            <div class="gsi-material-button-state"></div>
            <div class="gsi-material-button-content-wrapper">
              <div class="gsi-material-button-icon">
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"
                  xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block">
                  <path fill="#EA4335"
                    d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z">
                  </path>
                  <path fill="#4285F4"
                    d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z">
                  </path>
                  <path fill="#FBBC05"
                    d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z">
                  </path>
                  <path fill="#34A853"
                    d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z">
                  </path>
                  <path fill="none" d="M0 0h48v48H0z"></path>
                </svg>
              </div>
              <span class="gsi-material-button-contents">Sign up with Google</span>
              <span style="display: none">Sign up with Google</span>
            </div>
          </div>
        </a-form-item>
      </a-form>

      <div class="login-form-footer"></div>
      <Foot />
    </a-flex>
  </a-flex>
</template>
<script setup>
import { onMounted, reactive, ref } from "vue";
import { ArrowRightOutlined, LoadingOutlined } from "@ant-design/icons-vue";
import { validateEmail } from "@/utils/validate";
import { login, googleLogin, getProfile } from "@/api/auth";
import router from "@/router";
import LoginLeft from "./components/LoginLeft.vue";
import { setToken } from "@/utils/cache-token";
import { useUserStore } from "@/stores/user";
import Foot from "@/components/Foot.vue";
import { getToken } from "@/utils/cache-token";

const form = reactive({
  email: "",
  password: "",
  remember: true,
});
const userStore = useUserStore();
const disabled = ref(true);
const loading = ref(false);

const rules = reactive({
  email: [
    { required: true, message: "", trigger: "change" },
    { validator: validateEmail },
  ],
  password: [
    { required: true, trigger: "change", message: "" },
    // { validator: validatePass },
  ],
});

const onFinish = () => {
  if (loading.value) return;
  loading.value = true;
  login(form).then(res => {
    loading.value = false;
    if (res.is_authenticated) {
      console.log(res);
      setToken(res.id);
      userStore.setUser(res);
      if (!res.has_openai_secret_key) {
        router.push("/secretKey");
      } else {
        router.push("/dashboard");
      }
    }
  });
};

const googleAuth = () => {
  // googleLogin().then(res => {
  //   console.log(res);
  // });
  window.open("https://enzyhtp.app.vanderbilt.edu/api/auth/oauth/google/login", "_blank");
};

const handleValidate = (name, status) => {
  console.log(name, status);
  if (form.email && form.password) {
    disabled.value = !status;
  }
};

onMounted(() => {
  // const token = getToken();
  // console.log("mounted", userStore.user, token);
  // token &&
  getProfile().then(res => {
    console.log(res);
    if (res && res.is_authenticated) {
      setToken(res.id);
      userStore.setUser(res);
      if (!res.has_openai_secret_key) {
        router.push("/secretKey");
      } else {
        router.push("/dashboard");
      }
    }
  })
});
</script>
<style>
.forgot-password {
  margin-left: 210px;
  cursor: pointer;
}
</style>
