<template>
  <a-modal v-model:open="open" destroyOnClose @cancel="emit('update:open', false)" :title="title" :footer="null"
    width="35%" :bodyStyle="bodyStyle" wrapClassName="new-experiment-modal">
    <a-form :model="form" @validate="handleValidate" :rules="rules" layout="vertical" hideRequiredMark ref="formRef">
      <a-form-item label="Name" name="name">
        <a-input size="large" v-model:value="form.name" placeholder="Enter experiment name" />
      </a-form-item>
      <a-form-item label="Description">
        <a-input size="large" v-model:value="form.description" placeholder="Enter experiment description" />
      </a-form-item>

      <!-- <a-form-item label="Upload wild type" name="name">
				<a-upload-dragger v-model:fileList="fileList" name="file" :multiple="true"
					action="https://www.mocky.io/v2/5cc8019d300000980a055e76" @change="handleChange" @drop="handleDrop">
					<p class="theme-color">Drag and drop .pdb files here or click to upload</p>
				</a-upload-dragger>
			</a-form-item> -->

      <a-form-item>
        <a-flex class="btn-group">
          <div @click="emit('update:open', false)" class="btn">Cancel</div>
          <a-button type="primary" size="large" :disabled="disabled" @click="handleCreate" class="btn">
            <a-flex class="button-content" justify="space-between" align="center">
              <span>{{ experiment_id ? "Save" : "Create" }}</span>
              <LoadingOutlined v-if="loading" class="ml20" />
            </a-flex>
          </a-button>
        </a-flex>
      </a-form-item>
    </a-form>
  </a-modal>
</template>
<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import {
  createExperiment,
  updateExperimentProfile,
  getExperimentList,
} from "@/api/experiment";
import { message } from "ant-design-vue";
import { useExperimentStore } from "@/stores/experiment";
import { LoadingOutlined } from "@ant-design/icons-vue";
const experimentStore = useExperimentStore();

const bodyStyle = {
  // padding: '20px 24px',
};
const disabled = ref(true);
const loading = ref(false);

const open = defineModel({ type: Boolean, default: false });

const props = defineProps({
  experiment_id: { type: String, default: "" },
  name: { type: String, default: "" },
});

const emit = defineEmits(["ok", "update:open"]);

const form = reactive({
  name: "",
  description: "",
});

const title = computed(() => {
  return props.experiment_id ? "Rename experiment" : "New experiment";
});

const handleChange = info => {
  const status = info.file.status;
  if (status !== "uploading") {
  }
  if (status === "done") {
    message.success(`${info.file.name} file uploaded successfully.`);
  } else if (status === "error") {
    message.error(`${info.file.name} file upload failed.`);
  }
};

function handleDrop(e) { }

//
const getExperiment = () => {
  getExperimentList().then(res => {
    if (res.experiments) {
      experimentStore.setExperiments(res.experiments);
    }
  });
};

const handleCreate = () => {
  if (loading.value) return;
  loading.value = true;
  if (props.experiment_id) {
    updateExperiment();
  } else {
    createExperimentProfile();
  }
};

const createExperimentProfile = () => {
  createExperiment(form).then(res => {
    loading.value = false;
    if (res.is_successful) {
      getExperiment();
      message.success(res.message);
      emit("update:open", false);
      form.name = "";
    }
  });
};

const updateExperiment = () => {
  updateExperimentProfile(props.experiment_id, form).then(res => {
    loading.value = false;
    if (res.is_successful) {
      let item = experimentStore.experiments.find(
        item => item.id === props.experiment_id
      );
      if (item) {
        item.name = form.name;
      }
      experimentStore.experiment.name = form.name;

      message.success(res.message);
      emit("update:open", false);
    }
  });
};

const rules = reactive({
  name: [{ required: true, message: "", trigger: "change" }],
});

const handleValidate = (name, status) => {
  disabled.value = !status;
};

onMounted(() => {
  if (props.name) {
    form.name = props.name;
  }
});
const create = () => { };
</script>
<style lang="scss">
.new-experiment-modal {
  // .ant-modal-content,
  // .ant-modal-header {
  // 	background: #f4f4f4;
  // }

  .ant-btn-primary:disabled {
    background-color: #c6c6c6;
  }

  .ant-input-borderless:hover,
  .ant-input-borderless:focus,
  .ant-input,
  .ant-input-affix-wrapper,
  .ant-input-affix-wrapper>input.ant-input {
    background: #f4f4f4;
  }
}
</style>
