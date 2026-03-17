<template>
  <div class="tool-call-result">
    <!-- success message -->
    <a-flex justify="space-between" class="message-box success" v-if="showSuceessMessage">
      <div>
        <CheckCircleFilled style="font-size: 17px; color: #24a148; margin-right: 5px" />
        <span class="title ml10">{{ successTitle }}</span>
      </div>
      <div>
        <CloseOutlined style="color: #161616" class="ml40 icon" @click="showSuceessMessage = false" />
      </div>
    </a-flex>

    <!-- error message -->
    <a-flex justify="space-between" class="message-box error" v-if="showErrorMessage">
      <div @dblclick="reupload">
        <StopFilled style="font-size: 17px; color: #da1e28; margin-right: 5px" />
        <span class="title ml10">Upload failed.</span>
        <span>Please double check and try again. </span>
      </div>
      <div>
        <CloseOutlined style="color: #161616" class="ml40 icon" @click="showErrorMessage = false" />
      </div>
    </a-flex>

    <!-- confirm button -->
    <!--  -->
    <a-button type="primary" class="message-button" @click="confirmFn" v-if="showConfirmButton">
      <a-flex class="button-content" justify="space-between" align="center">
        <span>Confirm & continue</span>
        <LoadingOutlined v-if="loading" class="ml20" />
        <ArrowRightOutlined class="ml20" v-else />
      </a-flex>
    </a-button>

    <!-- select from 3D button -->
    <a-button type="primary" class="message-button" ghost v-if="show3DButton" @click="handleClick">
      <a-flex class="button-content" justify="space-between" align="center">
        <span>Select from 3D</span>
        <img src="@/assets/img/3d.svg" class="icon ml20" />
      </a-flex>
    </a-button>

    <!--  -->
    <a-upload-dragger :showUploadList="false" name="file" :multiple="false" class="upload-dragger" :action="actionUrl"
      @change="handleChange" @beforeUpload="handleBeforeUpload" @drop="handleDrop" v-show="showFileupload">
      <!-- <a-spin :spinning="uploadLoading"> -->
      <div class="ant-upload-text">
        Drag and drop .pdb files here or click to upload
      </div>
      <!-- </a-spin> -->
    </a-upload-dragger>
    <guiModal v-model="showGUI" v-if="showGUI" :experiment_id="props.experiment_id"></guiModal>
  </div>
</template>
<script setup>
import { ref, reactive, watch, computed } from "vue";
import {
  CloseOutlined,
  CheckCircleFilled,
  StopFilled,
  ArrowRightOutlined,
  LoadingOutlined,
} from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
import { pdb_fileValidation, updateAssistants } from "@/api/experiment";
import guiModal from "./guiModal.vue";
const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  // require_pdb_file: {
  //   type: Boolean,
  //   default: false,
  // },
  experiment_id: {
    type: String,
    default: "",
  },
  // confirm_button: {
  //   type: Boolean,
  //   default: false,
  // },
  from_3DButton: {
    type: Boolean,
    default: false,
  }
});

const emit = defineEmits(["confirmFn"]);

const successTitle = ref("");
const showSuceessMessage = ref(false);
const showErrorMessage = ref(false);
const isUpload = ref(false);
// const isShowConfirmButton = ref(true);
const show3DButton = ref(false);
const showGUI = ref(false);



const loading = ref(false);
const uploadKey = ref("upload");


const showFileupload = computed(() => {
  return isUpload.value ? false : props.data.require_pdb_file;
});

const showConfirmButton = computed(() => {
  console.log(props.data.confirm_button);
  return props.data.confirm_button;
});

watch(
  () => props.from_3DButton,
  () => {
    show3DButton.value = props.from_3DButton;
  }
);

const actionUrl = `/api/experiment/${props.experiment_id}/pdb_file`;

const handleClick = () => {
  showGUI.value = true;
};

const handleBeforeUpload = file => {
  return new Promise((resolve, reject) => {
    pdb_fileValidation({ file })
      .then(res => {
        if (res.is_successful) {
          resolve(file);
        } else {
          reject();
        }
      })
      .catch(() => {
      });
  });
};

const reupload = () => { };

const confirmFn = () => {
  if (loading.value) return;
  loading.value = true;
  updateAssistants(props.experiment_id).then(res => {
    loading.value = false;
    if (res.is_successful) {
      showSuceessMessage.value = true;
      successTitle.value = res.completion_message;
      // showConfirmButton.value = false;
      emit("confirmFn", {
        content: res.response_content,
        node: res.configuration_stages
      });
      // message.success(res.message);
      console.log(new Date().toLocaleString(), res.message)
      return;
    }
    message.error(res.message);
  });
};

const handleChange = info => {
  message.loading({ content: 'Loading...', key: uploadKey.value });
  console.log(info);
  const status = info.file.status;
  if (status !== "uploading") {
    console.log(info.file, info.fileList);
  }
  if (status === "done") {
    message.success({ content: `${info.file.name} file uploaded successfully.`, key: uploadKey.value, });
    successTitle.value = "Wild type uploaded!";
    showSuceessMessage.value = true;
    isUpload.value = true;
  } else if (status === "error") {
    message.error(`${info.file.name} file upload failed.`);
    showErrorMessage.value = true;
  }
};

function handleDrop(e) {
  console.log(e);
}
</script>
<style lang="scss" scoped>
.tool-call-result {
  margin-left: 32px;
}

.message-box {
  width: 761px;
  padding: 15px;
  // height: 48px;
  gap: 16px;
  border: 1px solid #0043ce4d;
  font-size: 14px;
  background: #edf5ff;
  box-shadow: 2px 0px 0px 0px #0043ce inset;

  &.success {
    background: #defbe6;
    border-color: #00bfa5;
    box-shadow: 2px 0px 0px 0px #24a148 inset;
  }

  &.error {
    background: #fff1f1;
    border-color: #da1e284d;
    box-shadow: 2px 0px 0px 0px #da1e28 inset;
  }

  .title {
    font-weight: 600;
    color: #161616;
  }

  .description {
    margin-left: 30px;
    width: 75%;
  }
}

.message-button {
  border-radius: 5px;
}

.message-box,
.message-button,
.upload-dragger {
  margin-top: 15px;
}

.ant-upload-wrapper.upload-dragger {
  width: 761px;
  height: 52px;
  display: block;
  text-align: center;
  color: #0f62fe;

  // margin: 0 auto;
}
</style>
