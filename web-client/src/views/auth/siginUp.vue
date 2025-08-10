<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Create an account</div>
        <div class="tip">
          <span>Have an account?</span>
          <span class="theme-color" @click="$router.push('/login')"
            >Log in</span
          >
        </div>
      </div>

      <a-form
        :model="form"
        layout="vertical"
        hideRequiredMark
        @validate="handleValidate"
        @finish="onFinish"
        :rules="rules"
        class="mt60"
        autocomplete="off"
      >
        <a-form-item label="Email address" name="email">
          <a-input v-model:value="form.email" :bordered="true" size="large" />
        </a-form-item>

        <!-- //validate-status="warning" -->
        <a-form-item label="Password" name="password">
          <a-input-password
            v-model:value="form.password"
            :bordered="true"
            size="large"
          />
        </a-form-item>

        <a-form-item>
          <a-button
            block
            type="primary"
            size="large"
            :disabled="disabled"
            html-type="submit"
          >
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span>Continue</span>
              <LoadingOutlined v-if="loading"/>
              <ArrowRightOutlined v-else/>
            </a-flex>
          </a-button>
        </a-form-item>
        <a-form-item>
          <div class="gsi-material-button" @click="googleAuth">
            <div class="gsi-material-button-state"></div>
            <div class="gsi-material-button-content-wrapper">
              <div class="gsi-material-button-icon">
                <svg
                  version="1.1"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 48 48"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  style="display: block"
                >
                  <path
                    fill="#EA4335"
                    d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
                  ></path>
                  <path
                    fill="#4285F4"
                    d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
                  ></path>
                  <path
                    fill="#FBBC05"
                    d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
                  ></path>
                  <path
                    fill="#34A853"
                    d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
                  ></path>
                  <path fill="none" d="M0 0h48v48H0z"></path>
                </svg>
              </div>
              <span class="gsi-material-button-contents"
                >Sign up with Google</span
              >
              <span style="display: none">Sign up with Google</span>
            </div>
          </div>

          <!-- <a-button block type="primary" ghost size="large" >
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span> Sign up with Google</span>
            </a-flex>
          </a-button> -->
        </a-form-item>
      </a-form>
      <Foot/>
    </a-flex>
  </a-flex>
</template>
<script setup>
import { reactive, ref } from "vue";
import { signUp, googleLogin } from "@/api/auth";
import { ArrowRightOutlined ,LoadingOutlined} from "@ant-design/icons-vue";
import { validatePass, validateEmail } from "@/utils/validate";
import LoginLeft from "./components/LoginLeft.vue";
import { message } from "ant-design-vue";
import Foot from "@/components/Foot.vue";
import router from "@/router";

const loading = ref(false);
const disabled = ref(true);

const form = reactive({
  email: "",
  password: "",
});

const rules = reactive({
  email: [
    { required: true, message: "", trigger: "change" },
    { validator: validateEmail },
  ],
  password: [
    { required: true, trigger: "change", message: `` },
    { validator: validatePass },
  ],
});

const onFinish = () => {
  if (loading.value) return;
  loading.value = true;
  signUp(form).then(res => {
    loading.value = false;
    if (res.is_successful) {
      message.success(res.message)
      router.push("/login");
      return
    }
    // message.error(res.message)
  });
};

const googleAuth = () => {
  // googleLogin().then(res => {
  //   console.log(res);
  // });
  window.open("https://enzyhtp.app.vanderbilt.edu/api/auth/oauth/google/login","_blank")
};

const handleValidate = (name, status) => {
  if (form.email && form.password) {
    disabled.value = !status;
  }
};
</script>
<style></style>
