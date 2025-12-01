<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Forgot Password</div>
        <div class="tip">
          <span
            >Please verify your email for us. Once you do, we'll send
            instructions to reset your password.</span
          >
        </div>
      </div>
      <a-form
        :model="form"
        layout="vertical"
        hideRequiredMark
        autocomplete="off"
        @finish="onFinish"
        @validate="handleValidate"
        :rules="rules"
        class="mt60"
      >
        <a-form-item label="Email address" name="email">
          <a-input v-model:value="form.email" :bordered="true" size="large" />
        </a-form-item>
        <a-form-item>
          <a-button
            block
            type="primary"
            size="large"
            html-type="submit"
            :loading="loading"
            :disabled="disabled"
            class="flex-ac"
          >
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span>Reset my password</span>
            </a-flex>
          </a-button>
        </a-form-item>
      </a-form>
      <Foot />
    </a-flex>
  </a-flex>
</template>
<script setup>
import LoginLeft from "./components/LoginLeft.vue";
import { h, reactive, ref } from "vue";
import { validateEmail } from "@/utils/validate";
import { resetGenerate } from "@/api/auth";
import { InfoCircleFilled } from "@ant-design/icons-vue";
import { notification } from "ant-design-vue";
import router from "@/router";
import Foot from "@/components/Foot.vue";

const disabled = ref(true);

const form = reactive({
  email: "",
});
const loading = ref(false);

const rules = reactive({
  email: [
    { required: true, message: "", trigger: "change" },
    { validator: validateEmail },
  ],
});

const openNotification = des => {
  notification.open({
    bottom: 50,
    message: h("div", {}, [
      h(InfoCircleFilled, { style: "color: #4589FF;" }),
      h(
        "span",
        { style: "margin-left: 20px;color:#fff;font-weight:bold" },
        "Instrction sent"
      ),
    ]),
    description: des,
    style: {
      width: "600px",
      background: "#393939",
      color: "#fff",
      borderLeft: "3px solid #4589FF",
      marginLeft: `${335 - 600}px`,
    },
    // class: "notification-custom-class",
  });
};

const handleValidate = (name, status) => {
  disabled.value = !status;
};

const onFinish = () => {
  if (loading.value) return;
  loading.value = true;
  resetGenerate(form)
    .then(res => {
      loading.value = false;
      if (res.is_successful) {
        openNotification(res.message);
        router.push({ path: "/resetPassword", query: { email: form.email } });
      }
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>
<style></style>
