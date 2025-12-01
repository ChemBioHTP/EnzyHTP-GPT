<template>
  <a-flex class="login-container">
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Change Password</div>
        <div class="tip">
          <span>Please enter your old password and new password.</span>
        </div>
      </div>

      <a-form
        :model="form"
        layout="vertical"
        hideRequiredMark
        autocomplete="off"
        @validate="handleValidate"
        @finish="onFinish"
        :rules="rules"
        class="mt30"
      >
        <a-form-item label="Old password" name="old_password">
          <a-input-password
            v-model:value="form.old_password"
            :bordered="true"
            size="large"
          />
        </a-form-item>
        <a-form-item label="New Password" name="new_password">
          <a-input-password
            v-model:value="form.new_password"
            :bordered="true"
            size="large"
          />
        </a-form-item>
        <a-form-item label="Confirm Password" name="confirm_password">
          <a-input-password
            v-model:value="form.confirm_password"
            :bordered="true"
            size="large"
          />
        </a-form-item>
        <a-form-item>
          <a-button
            block
            type="primary"
            size="large"
            html-type="submit"
            :disabled="disabled"
          >
            <a-flex
              class="button-content"
              justify="space-between"
              align="center"
            >
              <span>Change my password</span>
              <LoadingOutlined v-if="loading" class="ml20"/>
            </a-flex>
          </a-button>
        </a-form-item>
      </a-form>

      <div class="login-form-footer"></div>
    </a-flex>
  </a-flex>
</template>
<script setup>
import { ref, reactive } from "vue";
import { validatePass } from "@/utils/validate";
import { changePassword } from "@/api/auth";
import { useRouter } from "vue-router";
import { LoadingOutlined } from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
const emit = defineEmits(["ok"]);
const router = useRouter();
const form = reactive({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

const disabled = ref(true);
const loading = ref(false);

const validatePass2 = async (_rule, value) => {
  if (value === "") {
    return Promise.reject("Please input the password again");
  } else if (value !== form.new_password) {
    return Promise.reject("Two inputs don't match!");
  } else {
    return Promise.resolve();
  }
};

const rules = reactive({
  old_password: [{ required: true, message: "", trigger: "change" }],
  new_password: [
    { required: true, trigger: "change", message: `` },
    { validator: validatePass },
  ],
  confirm_password: [
    { required: true, trigger: "change", message: `` },
    { validator: validatePass2 },
  ],
});

const onFinish = () => {
  if(loading.value) return;
  loading.value = true;
  changePassword(form)
    .then(res => {
      loading.value = false;
      if (res.is_successful === true) {
        message.success(res.message);
        emit("ok");
        // setTimeout(() => {
          // router.push("/login");
        // }, 800);
      }
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleValidate = (name, status) => {
  if (form.old_password && form.new_password && form.confirm_password) {
    disabled.value = !status;
  }
};
</script>
<style scoped lang="scss">
.login-form {
  width: 480px;
  background-color: #fff;
  color: #000;
  padding: 0;

  .login-form-header {
    user-select: none;
    .title {
      font-size: 36px;
      line-height: 44px;
      font-weight: 300;
    }

    .tip {
      font-size: 16px;
      line-height: 24px;
      margin-top: 20px;

      .theme-color {
        margin-left: 5px;
        cursor: pointer;
      }
    }
  }
}
</style>
