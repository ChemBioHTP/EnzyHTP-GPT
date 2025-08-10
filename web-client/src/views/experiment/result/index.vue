<script setup>
import { onMounted, reactive, ref, h, watch } from "vue";

import HeadInfo from "@/views/experiment/components/headInfo.vue";
import { getExperimentDetail } from "@/api/experiment";
import { getAssistantList, getMutations } from "@/api/experiment";
import { useRoute } from "vue-router";
import InputResult from "@/views/experiment/components/inputResult.vue";
import InputComponent from "./components/input.vue";
import { useExperimentStore } from "@/stores/experiment";
import ResultComponent from "./components/result.vue";
const experimentStore = useExperimentStore();

const route = useRoute();
const experiment = ref({});
const spinning = ref(false);

const model = reactive({
  messageList: [],
  node: [],
  mutations: [],
});

const selected = ref("Input");

watch(
  () => route.query.id,
  () => {
    init();
  }
);


const getExperiment = async () => {
  spinning.value = true;
  getExperimentDetail(route.query.id).then(res => {
    // spinning.value = false;
    experiment.value = res;
    experimentStore.setExperiment(res);
    let item = experimentStore.experiments.find(item => item.id == route.query.id);
    if (item) {
      item._status = res.status;
    }
  });
};

const getMutationsList = () => {
  getMutations(route.query.id).then(res => {
    if (res.is_successful) {
      model.mutations = res.mutant_string_list;
    }
    console.log(res, "getMutations");
  });
};

const getAssistant = () => {
  getAssistantList(route.query.id).then(res => {
    spinning.value = false;
    model.messageList = res.assistant_messages ?? [];
    model.node = res.configuration_stages ?? [];

    console.log(model.messageList);
  });
};
const init = () => {
  getExperiment();
  getMutationsList();
  getAssistant();
};


if (route.query.type) {
  selected.value = route.query.type;
}

onMounted(() => {
  init();
});
</script>

<template>
  <a-flex class="container">
    <div class="box">
      <a-spin :spinning="spinning">
        <HeadInfo :experiment="experimentStore.experiment" />
        <InputResult v-model="selected" />
        <InputComponent v-show="selected === 'Input'" :node="model.node" :messageList="model.messageList"
          :mutations="model.mutations" />
        <ResultComponent :progress="Number(experiment.progress*100)" :mutations="model.mutations"
          v-show="selected === 'Results'" :status="experiment.status" />
      </a-spin>
    </div>
  </a-flex>
</template>
<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;

  .box {
    flex: 1;
    width: 100%;
    height: 100%;
  }
}
</style>
