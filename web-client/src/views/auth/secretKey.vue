<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Provider and API Key</div>
        <div class="tip">
          <span>Select your model provider and model first.</span>
          <div class="tip-warning">OpenAI requires your own API key. Fireworks can use server default key by default.</div>
          <a
            class="theme-color"
            :href="learnMoreLink"
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
        class="mt60"
      >
        <a-form-item label="Provider" name="openai_provider">
          <a-select
            v-model:value="form.openai_provider"
            size="large"
            :options="providerOptions"
            :disabled="profileLoading"
            @change="handleProviderChange"
          />
        </a-form-item>

        <a-form-item label="Model" name="openai_model">
          <a-select
            v-model:value="form.openai_model"
            size="large"
            :options="modelOptions"
            :disabled="profileLoading"
          />
        </a-form-item>

        <a-form-item v-if="form.openai_provider === 'fireworks'" name="use_custom_openai_secret_key">
          <a-checkbox v-model:checked="form.use_custom_openai_secret_key" :disabled="profileLoading">
            Use my own API key (optional)
          </a-checkbox>
        </a-form-item>

        <a-form-item label="API key" name="openai_secret_key">
          <a-input
            v-model:value="form.openai_secret_key"
            :bordered="true"
            size="large"
            :disabled="profileLoading || !requireApiKey"
            :placeholder="requireApiKey ? 'Enter your API key' : 'Using server default key'"
          />
        </a-form-item>

        <a-form-item>
          <a-button block type="primary" size="large" html-type="submit" :disabled="disabled">
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
import { reactive, ref, computed, onMounted } from "vue";
import { message as antdMessage } from "ant-design-vue";
import LoginLeft from "./components/LoginLeft.vue";
import { logout, updateProfile, getProfile } from "@/api/auth";
import Foot from "@/components/Foot.vue";
import { ArrowRightOutlined, LoadingOutlined } from "@ant-design/icons-vue";
import router from "@/router";
import {
  LLM_MODEL_OPTIONS,
  LLM_PROVIDER_OPTIONS,
  getDefaultModelByProvider,
  requiresApiKey,
} from "@/config/llm";

const form = reactive({
  openai_provider: "openai",
  openai_model: getDefaultModelByProvider("openai"),
  use_custom_openai_secret_key: true,
  openai_secret_key: "",
});

const signOutLoading = ref(false);
const loading = ref(false);
const profileLoading = ref(true);
const providerOptions = LLM_PROVIDER_OPTIONS;
const modelOptions = computed(() => LLM_MODEL_OPTIONS[form.openai_provider] || []);
const requireApiKey = computed(() =>
  requiresApiKey(form.openai_provider, form.use_custom_openai_secret_key)
);
const disabled = computed(() => {
  if (profileLoading.value) return true;
  if (loading.value) return true;
  if (!form.openai_provider || !form.openai_model) return true;
  if (requireApiKey.value && !form.openai_secret_key) return true;
  return false;
});
const learnMoreLink = computed(() => {
  if (form.openai_provider === "fireworks") {
    return "https://docs.fireworks.ai/";
  }
  return "https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key";
});

const syncModelForProvider = () => {
  const providerModelOptions = LLM_MODEL_OPTIONS[form.openai_provider] || [];
  if (!providerModelOptions.find(option => option.value === form.openai_model)) {
    form.openai_model = getDefaultModelByProvider(form.openai_provider);
  }
};

const handleProviderChange = provider => {
  if (provider === "openai") {
    form.use_custom_openai_secret_key = true;
  } else if (provider === "fireworks") {
    form.use_custom_openai_secret_key = false;
  }
  syncModelForProvider();
};

const loadProfile = async () => {
  profileLoading.value = true;
  try {
    const res = await getProfile();
    const provider = res?.openai_provider || "openai";
    form.openai_provider = provider;
    form.openai_model = res?.openai_model || getDefaultModelByProvider(provider);
    form.use_custom_openai_secret_key = provider === "openai"
      ? true
      : !!res?.use_custom_openai_secret_key;
    syncModelForProvider();
  } catch {
    antdMessage.error("Failed to load current provider settings.");
  } finally {
    profileLoading.value = false;
  }
};

const onFinish = () => {
  if (profileLoading.value || loading.value) return;
  loading.value = true;
  const payload = {
    openai_provider: form.openai_provider,
    openai_model: form.openai_model,
    use_custom_openai_secret_key: form.use_custom_openai_secret_key,
  };
  if (requireApiKey.value || form.openai_secret_key) {
    payload.openai_secret_key = form.openai_secret_key;
  }

  updateProfile(payload)
    .then(res => {
      loading.value = false;
      if (res.is_successful === true) {
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

onMounted(() => {
  loadProfile();
});
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
