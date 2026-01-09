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
                >Update OpenAI key</a
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
        <div class="title">Provide Secret API Key</div>
        <div class="tip">
          <span>Copy and paste your API key from OpenAI.</span>
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
        class="mt60"
        :rules="rules"
        @finish="onFinish"
        @validate="handleValidate"
      >
        <a-form-item label="" name="openai_secret_key">
          <a-input
            v-model:value="form.openai_secret_key"
            :bordered="true"
            size="large"
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
import { ref, reactive } from "vue";
import { ArrowLeftOutlined } from "@ant-design/icons-vue";
import { logout, updateProfile } from "@/api/auth";
import ChangePassword from "@/views/auth/changePassword.vue";
import { message } from "ant-design-vue";
import { useExperimentStore } from "@/stores/experiment";
const experimentStore = useExperimentStore();

const logOut = async () => {
  await logout();
  experimentStore.setExperiments([]);
  experimentStore.setExperiment({})
};
const disabled = ref(true);
const loading = ref(false);

const form = reactive({
  openai_secret_key: "",
});
const rules = reactive({
  openai_secret_key: [{ required: true, message: "", trigger: "change" }],
});
const model = reactive({
  openChangePassword: false,
  openUpdateOpenAIKey: false,
});

const changePassword = () => {
  model.openChangePassword = true;
};
const updateOpenAIKey = () => {
  model.openUpdateOpenAIKey = true;
};

const onFinish = async () => {
  if(loading.value) return;
  loading.value = true;
  updateProfile(form).then(res => {
    loading.value = false;
    if (res.is_successful === true&&res.is_openai_secret_key_valid) {
      message.success(res.message);
      form.openai_secret_key = "";
      model.openUpdateOpenAIKey = false;
      return;
    }
    message.error(res.message);
  });
};

const handleValidate = (name, status) => {
  if (form.openai_secret_key) {
    disabled.value = !status;
  }
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
  }
}
</style>
