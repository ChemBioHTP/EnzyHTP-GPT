<template>
  <div class="header-info">
    <a-flex justify="space-between" align="center">
      <div class="left">
        <div class="theme-color" @click="$router.push('/dashboard')">
          Back to all experiments
        </div>
        <div class="mt10">
          <span class="title">{{ experiment?.name }}</span>
          <span :class="[
            getClass(experiment?.status)
          ]"></span>
          <span class="status">
            {{ experiment?.status_text }}
          </span>
        </div>
      </div>
      <div>
        <a-dropdown placement="bottom" overlayClassName="headInfo-dropdown">
          <img src="@/assets/img/more-icon.svg" class="icon" alt="" srcset="" />
          <template #overlay>
            <a-menu>
              <a-menu-item>
                <a-button size="small" style="color: #525252" type="link" @click="open = true">Rename</a-button>
              </a-menu-item>
              <a-menu-item>
                <a-button size="small" style="color: #525252" type="link" @click="deleteShow = true">Delete</a-button>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
        <img src="@/assets/img/info.svg" class="ml40 icon" alt="" srcset="" />
      </div>
    </a-flex>
    <ExperimentModal v-if="experiment" v-model:open="open" :experiment_id="experiment.id" :name="experiment.name" />

    <a-modal v-model:open="deleteShow" destroyOnClose @cancel="deleteShow = false" title="Delete experiment?"
      :footer="null" width="35%" :bodyStyle="bodyStyle" wrapClassName="new-experiment-modal">
      <a-form :model="form" @validate="handleValidate" :rules="rules" layout="vertical" hideRequiredMark ref="formRef">
        <div>Are you sure you want to delete this experiment?</div>
        <div style="margin-bottom: 60px">This action cannot be undone.</div>
        <a-form-item>
          <a-flex class="btn-group">
            <div @click="deleteShow = false" class="btn">Cancel</div>
            <a-button type="primary" style="background: #da1e28" size="large" :disabled="disabled"
              @click="deleteConfirm" class="btn">
              <a-flex class="button-content" justify="space-between" align="center">
                <span>Delete experiment</span>
                <LoadingOutlined v-if="loading" />
              </a-flex>
            </a-button>
          </a-flex>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>
<script setup>
import { ref } from "vue";
import ExperimentModal from "@/components/ExperimentModal.vue";
import { message } from "ant-design-vue";
import { delExperiment } from "@/api/experiment";
import { useExperimentStore } from "@/stores/experiment";
import { useRouter } from "vue-router";
import { LoadingOutlined } from "@ant-design/icons-vue";

const experimentStore = useExperimentStore();
const router = useRouter();

const props = defineProps({
  experiment: {
    type: Object,
    required: true,
  },
});

// const experiment = ref(experimentStore.experiment)
const open = ref(false);
const deleteShow = ref(false);

const loading = ref(false);

const getClass = (status) => {
  console.log(status)
  if (status > 0) {
    return 'status-dot2'
  } else if (status == -3 || status == -8) {
    return 'status-dot-8'
  } else if (status >= -9 && status <= -1) {
    return 'status-dot-9'
  } else {
    return 'status-dot0'
  }
};

const deleteConfirm = () => {
  if (loading.value) return;
  loading.value = true;
  delExperiment({ experiment_id: props.experiment.id }).then(res => {
    loading.value = false;
    if (res.is_successful) {
      let list = experimentStore.experiments.filter(
        item => item.id !== props.experiment.id
      );

      experimentStore.setExperiments(list);

      message.success(res.message);
      deleteShow.value = false;
      router.push("/dashboard");
    }
  });
};
</script>
<style scoped lang="scss">
.header-info {
  font-size: 14px;
  padding: 16px 32px;
  border-bottom: 1px solid #e0e0e0;
  height: 104px;

  .left {
    .theme-color {
      cursor: pointer;
    }
  }

  .title {
    font-size: 36px;
    font-weight: 600;
    line-height: 44px;
  }

  .status {
    font-size: 14px;
    font-weight: 400;
    line-height: 20px;
    // margin-left: 44px;
    color: #525252;
    position: relative;
  }

  .status-dot-9,
  .status-dot2,
  .status-dot-8,
  .status-dot-3,
  .status-dot0 {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    margin: 0 10px 0 40px;
  }

  .status-dot-9 {
    background-color: #f1c21b;
  }

  .status-dot-8 {
    background-color: #40e0d0;
  }

  // .status-dot-3 {
  //   background-color: #0f62fe;
  // }

  .status-dot0 {
    background-color: #00b39f;
  }

  .status-dot2 {
    background-color: #da1e28;
  }
}
</style>
