<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Provide Secret API Key</div>
        <div class="tip">
          <span>Copy and paste your API key from OpenAI.</span>
          <div class="tip-warning">NOTE: The OpenAI account for this key must have available funds. (>$1)</div>
          <a
            class="theme-color"
            href="https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn more
          </a>
        </div>
      </div>

      <a-form
        :model="form"
        layout="vertical"
        hideRequiredMark
        autocomplete="off"
        @finish="onFinish"
        :rules="rules"
        @finishFailed="onFinishFailed"
        class="mt60"
      >
        <a-form-item label="API key" name="openai_secret_key">
          <a-input v-model:value="form.openai_secret_key" :bordered="true" size="large" />
        </a-form-item>

        <a-form-item>
          <a-button block type="primary" size="large" html-type="submit">
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span>Continue</span>
              <LoadingOutlined v-if="loading" />
              <ArrowRightOutlined v-else />
            </a-flex>
          </a-button>
        </a-form-item>
        <div
          @click="signOut"
          class="sign-out-button custom-button mt10 width100"
        >
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Sign out</span>
            <span><LoadingOutlined v-if="signOutLoading" /></span>
          </a-flex>
        </div>
      </a-form>
      <div class="login-form-footer"></div>
      <Foot/>
    </a-flex>
  </a-flex>
</template>
<script setup>
import { reactive, ref } from "vue";
import { message as antdMessage } from "ant-design-vue";
import LoginLeft from "./components/LoginLeft.vue";
import { logout ,updateProfile} from "@/api/auth";
import Foot from "@/components/Foot.vue";
import { ArrowRightOutlined, LoadingOutlined } from "@ant-design/icons-vue";
import router from "@/router";
const form = reactive({
  openai_secret_key: "",
});

const rules = reactive({
  openai_secret_key: [
    {
      required: true,
      message: "",
      trigger: "change",
    },
  ],
});
const signOutLoading = ref(false);
const loading = ref(false);

const onFinish = () => {
  // TODO: validate API key
  if (loading.value) return;
  loading.value = true;
  updateProfile(form)
    .then(res => {
      loading.value = false;
      if (res.is_successful === true && res.is_openai_secret_key_valid) {
        antdMessage.success(res.message);
        form.openai_secret_key = "";
        router.push("/dashboard");
        return;
      }
      const errMsg = res?.message || res?.openai_response_description || "Invalid OpenAI Secret Key.";
      antdMessage.error(errMsg);
    })
    .catch(() => {
      loading.value = false;
      antdMessage.error("Network or server error, please try again.");
    });
};

const signOut = async () => {
  if (signOutLoading.value) return;
  signOutLoading.value = true;
  await logout().then(() => {
    signOutLoading.value = false;
  });
};
</script>
<style scoped>
.sign-out-button {
  background-color: #393939;
  color: #fff;
}
.tip-warning {
  color: #2534d9;
}
</style>
