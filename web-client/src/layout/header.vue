<template>
  <a-flex class="header" justify="space-between" align="center">
    <div class="logo">MutexaGPT</div>
    <div class="user-info">
      <img src="@/assets/img/message-icon.png" alt="" />
      <a-dropdown placement="bottomLeft" overlayClassName="head-dropdown">
        <img src="@/assets/img/user-icon.png" alt="" class="ml20" />
        <template #overlay>
          <a-menu>
            <a-menu-item>
              <a href="javascript:;" @click="changePassword">Change password</a>
            </a-menu-item>
            <a-menu-divider />
            <a-menu-item>
              <a href="javascript:;" @click="updateOpenAIKey"
                >Config AI Provider/Model</a
              >
            </a-menu-item>
            <a-menu-divider />
            <a-menu-item>
              <a href="javascript:;" @click="logOut">Sign out</a>
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </a-flex>
  <!-- Change Password Modal -->
  <div v-if="model.openChangePassword" class="custom-class">
    <div class="login-form">
      <div>
        <ArrowLeftOutlined
          style="font-size: 25px; margin-bottom: 20px; cursor: pointer"
          @click="model.openChangePassword = false"
        />
      </div>
      <ChangePassword @ok="model.openChangePassword = false"></ChangePassword>
    </div>
  </div>
  <!-- Update OpenAI Key Modal -->
  <div class="custom-class" v-if="model.openUpdateOpenAIKey">
    <div class="login-form">
      <div>
        <ArrowLeftOutlined
          style="font-size: 25px; margin-bottom: 20px; cursor: pointer"
          @click="model.openUpdateOpenAIKey = false"
        />
      </div>
      <div class="login-form-header">
        <div class="title">Set Your Provider and API Key</div>
        <div class="tip">
          <span>Select your provider and model first.</span>
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
        class="mt60"
        @finish="onFinish"
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
          <a-button
            block
            type="primary"
            size="large"
            class="btn-48"
            html-type="submit"
            :disabled="disabled"
          >
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span>Update</span>
              <LoadingOutlined v-if="loading" class="ml20"/>
            </a-flex>
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, computed } from "vue";
import { ArrowLeftOutlined, LoadingOutlined } from "@ant-design/icons-vue";
import { logout, updateProfile, getProfile } from "@/api/auth";
import ChangePassword from "@/views/auth/changePassword.vue";
import { message } from "ant-design-vue";
import { useExperimentStore } from "@/stores/experiment";
import {
  LLM_MODEL_OPTIONS,
  LLM_PROVIDER_OPTIONS,
  getDefaultModelByProvider,
  requiresApiKey,
} from "@/config/llm";
const experimentStore = useExperimentStore();

const logOut = async () => {
  await logout();
  experimentStore.setExperiments([]);
  experimentStore.setExperiment({})
};
const loading = ref(false);
const profileLoading = ref(false);

const form = reactive({
  openai_provider: "openai",
  openai_model: getDefaultModelByProvider("openai"),
  use_custom_openai_secret_key: true,
  openai_secret_key: "",
});
const model = reactive({
  openChangePassword: false,
  openUpdateOpenAIKey: false,
});
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

const changePassword = () => {
  model.openChangePassword = true;
};
const updateOpenAIKey = async () => {
  if (profileLoading.value) return;
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
    model.openUpdateOpenAIKey = true;
  } catch {
    message.error("Failed to load current provider settings.");
  } finally {
    profileLoading.value = false;
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

const onFinish = async () => {
  if(profileLoading.value || loading.value) return;
  loading.value = true;
  const payload = {
    openai_provider: form.openai_provider,
    openai_model: form.openai_model,
    use_custom_openai_secret_key: form.use_custom_openai_secret_key,
  };
  if (requireApiKey.value || form.openai_secret_key) {
    payload.openai_secret_key = form.openai_secret_key;
  }
  updateProfile(payload).then(res => {
    loading.value = false;
    if (res.is_successful === true) {
      message.success(res.message);
      form.openai_secret_key = "";
      model.openUpdateOpenAIKey = false;
      return;
    }
    message.error(res.message);
  });
};
</script>
<style lang="scss" scoped>
.header {
  height: 48px;
  background-color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;

  .logo {
    color: #fff;
    font-size: 14px;
    letter-spacing: 3px;
    font-weight: 700;
    cursor: pointer;
    user-select: none;
  }

  .user-info {
    img {
      width: 16px;
      height: 16px;
      cursor: pointer;
    }
  }
}

.custom-class {
  position: fixed;
  left: 48px;
  top: 50px;
  padding: 20px;
  z-index: 10;
  background-color: #fff;
  width: 100%;
  height: 100%;

  .login-form {
    width: 400px;
  }
  .login-form-header {
    user-select: none;
    .title {
      font-size: 25px;
      line-height: 44px;
      font-weight: 300;
    }

    .tip {
      font-size: 13px;
      line-height: 24px;
      // margin-top: 20px;

      .theme-color {
        margin-left: 5px;
        cursor: pointer;
      }
    }
    .tip-warning {
      color: #2534d9;
    }
  }
}
</style>
