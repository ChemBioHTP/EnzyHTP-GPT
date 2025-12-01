<template>
  <a-flex class="login-container">
    <LoginLeft />
    <a-flex class="login-form" vertical justify="center">
      <div class="login-form-header">
        <div class="title">Reset Password</div>
        <div class="tip">
          <span>Please enter your new password.</span>
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
        class="mt60"
      >
        <!-- //validate-status="warning" -->

        <a-form-item label="Verification code" name="verification_code">
          <a-input
            v-model:value="form.verification_code"
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

      <div class="login-form-footer"></div>
      <Foot/>
    </a-flex>
  </a-flex>
</template>
<script setup>
import { ref, reactive } from "vue";
import LoginLeft from "./components/LoginLeft.vue";
import { validatePass } from "@/utils/validate";
import { resetPassword } from "@/api/auth";
import Foot from "@/components/Foot.vue";

import router from "@/router";
import { useRoute } from "vue-router";
const route = useRoute();

// import { useUserStore } from "@/stores/user";

const form = reactive({
  verification_code: "",
  new_password: "",
  confirm_password: "",
});

// const userStore = useUserStore();
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
  verification_code: [{ required: true, message: "", trigger: "change" }],
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
  resetPassword({ ...form, email: route.query.email })
    .then((res) => {
      if(res.is_successful===true){
        router.push("/login");
      }
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleValidate = (name, status) => {
  if (form.verification_code && form.new_password && form.confirm_password) {
    disabled.value = !status;
  }
};
</script>
<style></style>
