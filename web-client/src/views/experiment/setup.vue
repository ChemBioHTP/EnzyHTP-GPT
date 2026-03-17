<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { ArrowRightOutlined } from "@ant-design/icons-vue";
import VerticalStepper from "@/components/VerticalStepper.vue";
import HeadInfo from "./components/headInfo.vue";
import { getExperimentDetail, getAssistantList } from "@/api/experiment";
import { useExperimentStore } from "@/stores/experiment";
import Chart from "./components/chart.vue";
import NodeList from "./components/nodeList.vue";
import { useRoute, useRouter } from "vue-router";
const experimentStore = useExperimentStore();

const route = useRoute();

const router = useRouter();

const experiment = ref({});

const spinning = ref(false);

const steps = reactive([
  {
    title: "Set-up",
    icon: "process",
  },
  {
    title: "Workflow",
    icon: "wait",
    disabled: true,
  },
]);

const node = ref([]);

const model = reactive({
  messageList: [],
});

const getMessages = (show = true) => {
  spinning.value = show;
  getAssistantList(route.query.id).then(res => {
    model.messageList = res.assistant_messages ?? [];
    node.value = res.configuration_stages ?? [];
    if (res.require_pdb_file || res.confirm_button) {
      model.messageList = [
        ...model.messageList,
        {
          data: {
            require_pdb_file: res.require_pdb_file,
            confirm_button: res.confirm_button,
          },
        },
      ];
    }
    spinning.value = false;
  });
};

const handleStep = (index) => {
  console.log(index, "handleStep");
  if (index == 1) {
    router.push({ path: "/workFlow", query: { id: route.query.id } });
  }
}

const nextDisabled = computed(() => {
  return (
    node.value.length === 0 || !node.value.every(item => item.is_completed)
  );
});

const showNode = computed(() => {
  return node.value.filter(item => item.is_completed).length > 0;
});

const getNode = (res) => {
  // getAssistantList(route.query.id).then(res => {
  node.value = res ?? [];
  // });
};

watch(
  () => route.query.id,
  () => {
    init();
  }
);

const getExperiment = async () => {
  spinning.value = true;
  getExperimentDetail(route.query.id).then(res => {
    experiment.value = res;
    experimentStore.setExperiment(res);
    if (res.assistant_conversation_completed) {
      steps[1].disabled = false;
      if (!route.query.type) {
        handleNext();
      }
    }
  });
};

const init = () => {
  model.messageList = [];
  node.value = [];
  getExperiment();
  getMessages();
};

const handleNext = () => {
  router.push({ path: "/workFlow", query: { id: experiment.value.id } });
};

onMounted(() => {
  init();
});
</script>

<template>
  <a-flex class="container">
    <div class="box container">
      <a-spin :spinning="spinning" v-if="spinning" class="spinning"></a-spin>
      <div v-show="!spinning" class="container">
        <HeadInfo :experiment="experimentStore.experiment" v-if="!spinning" />
        <a-flex class="box-content" justify="space-between">
          <VerticalStepper :steps="steps" @change="handleStep" class="steps mt30" />
          <div class="chart-content">
            <Chart :default-message="model.messageList" @send="getNode" />
          </div>
          <div class="list">
            <NodeList :node="node" />
          </div>
        </a-flex>
        <a-flex class="footer" justify="end">
          <a-button type="primary" size="large" style="width: 134px;" @click="handleNext"
            :disabled="nextDisabled">
            <a-flex class="button-content" justify="space-between" align="center">
              <span>Next</span>
              <ArrowRightOutlined />
            </a-flex>
          </a-button>
        </a-flex>
      </div>
    </div>
  </a-flex>
</template>
<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;

  .box {
    flex: 1;
    position: relative;

    .box-content {
      height: calc(100% - 210px);
      width: 100%;
      padding: 0 32px;
      overflow: hidden;

      .steps {
        width: 220px;
        height: 116px;
      }

      .chart-content {
        width: 64%;
      }

      .list {
        width: 280px;
        border-left: 1px solid #e0e0e0;
        padding: 30px 17px;
        margin-left: 15px;
      }
    }

    .footer {
      border-top: 1px solid #e0e0e0;
      height: 100px;
      overflow: hidden;
      display: flex;
      align-items: center;

      .ant-btn.ant-btn-lg {
        height: 48px;
        margin-right: 35px;
      }
    }
  }
}
</style>
