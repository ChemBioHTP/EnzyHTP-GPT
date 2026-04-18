<template>
  <a-flex class="content">
    <div class="steps">
      <VerticalStepper :steps="stpes" v-model="currentStep" style="height: 140px" />
    </div>
    <!-- <div> -->
    <div v-show="currentStep === 0" class="flex width100">
      <div class="chart-content">
        <!-- <a-spin :spinning="spinning"> -->
        <div class="message" v-if="model.chartTip">
          <a-flex justify="space-between">
            <div>
              <ExclamationCircleFilled
                style="font-size: 17px; color: #0043ce; margin-right: 5px"
              />
              <span class="title ml10">Read-Only Inputs</span>
            </div>
            <div>
              <span class="theme-color" style="cursor: pointer">Duplicate</span>
              <CloseOutlined
                style="font-size: 15px; color: #161616"
                class="ml40 icon"
                @click="model.chartTip = false"
              />
            </div>
          </a-flex>
          <div class="description">
            Once an experiment is finalized, its inputs become read-only. To
            make adjustments and re-run, please duplicate the experiment
          </div>
        </div>
        <Chart :defaultMessage="messageList" :preivew="true" />
        <!-- <a-empty v-else description="No messages found" class="mt20" /> -->
        <!-- </a-spin> -->
      </div>
      <div class="list">
        <NodeList :node="node" />
      </div>
    </div>
    <div v-show="currentStep === 1" class="flex width100">
      <div class="chart-content">
        <a-flex justify="end" class="download-row">
          <a-button
            size="large"
            :loading="downloading"
            @click="handleExportAccrePack"
          >
            Export Reproducibility package
          </a-button>
        </a-flex>
        <div class="message" v-if="model.workflowTip">
          <a-flex justify="space-between">
            <div>
              <ExclamationCircleFilled
                style="font-size: 17px; color: #0043ce; margin-right: 5px"
              />
              <span class="title ml10">Read-Only Inputs</span>
            </div>
            <div>
              <span class="theme-color" style="cursor: pointer">Duplicate</span>
              <CloseOutlined
                style="font-size: 15px; color: #161616"
                class="ml40 icon"
                @click="model.workflowTip = false"
              />
            </div>
          </a-flex>
          <div class="description">
            Once an experiment is finalized, its inputs become read-only. To
            make adjustments and re-run, please duplicate the experiment
          </div>
        </div>
        <div class="mt10">
          <WorkFlowConfig :show="true" :constraints="constraints" />
        </div>
      </div>
      <div class="list">
        <MutationGenerrated :mutations="mutations"/>
      </div>
    </div>
    <!-- </div> -->
  </a-flex>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue";
import { ExclamationCircleFilled, CloseOutlined } from "@ant-design/icons-vue";
import Chart from "@/views/experiment/components/chart.vue";
import VerticalStepper from "@/components/VerticalStepper.vue";
import NodeList from "@/views/experiment/components/nodeList.vue";
import { useRoute } from "vue-router";
import MutationGenerrated from "@/views/experiment/components/mutationGenerrated.vue";
import WorkFlowConfig from "@/views/experiment/components/workFlowConfig.vue";
import { deployAccre } from "@/api/experiment";
import { downloadFile } from "@/utils/common";
const route = useRoute();

const props = defineProps({
  messageList: {
    type: Array,
    default: () => [],
  },
  node: {
    type: Array,
    default: () => [],
  },
  mutations: {
    type: Array,
    default: () => [],
  },
  constraints: {
    type: Array,
    default: () => [],
  },
});

const stpes = reactive([
  {
    title: "Set-up",
    icon: "finish",
  },
  {
    title: "Workflow",
    icon: "finish",
  },
]);
const currentStep = ref(0);
const downloading = ref(false);
const model = reactive({
  // messageList: [],
	// node: [],
	// mutations: [],
  chartTip: true,
  workflowTip: true,
});

const handleExportAccrePack = () => {
  if (downloading.value) return;
  downloading.value = true;
  deployAccre(route.query.id)
    .then(res => {
      downloadFile(res, "accre-run-pack.zip");
    })
    .finally(() => {
      downloading.value = false;
    });
};


onMounted(() => {
 
});
</script>
<style lang="scss" scoped>
.content {
  height: 65vh;
  width: 100%;
  padding: 0 32px;

  .steps {
    width: 300px;
  }

  .message {
    // width: 761px;
    padding: 15px;
    gap: 16px;
    border: 1px solid #0043ce4d;
    font-size: 14px;
    background: #edf5ff;
    box-shadow: -3px 0px 0px 0px #0043ce;

    .title {
      font-size: 14px;
      font-weight: 600;
      color: #161616;
    }

    .description {
      margin-left: 30px;
      width: 75%;
    }
  }

  .chart-content {
    width: 70%;

    .description {
      margin-top: 15px;
    }

    .download-row {
      margin-bottom: 12px;
    }
  }

  .list {
    width: 320px;
    border-left: 1px solid #e0e0e0;
    margin-left: 15px;
    padding-left: 15px;
  }

  .description {
    color: #525252;
    font-size: 14px;
    font-weight: 400;
  }
}
</style>
