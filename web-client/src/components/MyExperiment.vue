<template>
  <div class="my-experiment">
    <div class="status-list">
      <div class="header">
        <span class="title">My experiments</span>
        <img src="" alt="" srcset="" />
      </div>
      <ul class="list">
        <li v-for="(item, index) in statusList" :key="item.name" @click="change(index)"
          :class="{ active: selectSatus === index }">
          {{ item.name }}
        </li>
      </ul>
    </div>
    <div class="line"></div>
    <div class="experiment-list">
      <a-spin :spinning="spinning">
        <ul class="list">
          <template v-for="item in showList" :key="item.name">
            <a-tooltip placement="right" :title="item.name">
              <li @click="openExperiment(item)" :class="{ active: selectExperiment === item.id }">
                {{ item.name }}
              </li>
            </a-tooltip>
          </template>
        </ul>
      </a-spin>
    </div>
  </div>
</template>
<script setup>
import { computed, onActivated, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useExperimentStore } from "@/stores/experiment";

const experimentStore = useExperimentStore();

const router = useRouter();

const route = useRoute();

const selectSatus = ref(experimentStore.experimentType ?? 0);

const selectExperiment = ref(route.query.id ?? "");

const spinning = ref(false);

// selectExperiment.value = route.query.id || "";

watch(
  () => route.query.id,
  () => {
    if (route.query.id) {
      selectExperiment.value = route.query.id;
    } else {
      selectExperiment.value = "";
    }
  }
);

const emit = defineEmits(["change", "openExperiment"]);

const statusList = ref([
  { name: "All", status: "All" },
  { name: "In progress", status: [-9, -8, -7, -6, -5, -4, -3, -2, -1] },
  { name: "With error", status: [1, 2, 3] },
  { name: "Complete", status: [0] },
  { name: "Archived", status: [] },
]);

/**
 * In progress 包含 status 为 -9 到 -1；
With error 包含 status 为 1 到 3；
Complete 单单指 status 为 0；
Archieved 还没有对应的值，我之后加一个给你吧。

 */

const showList = computed(() => {
  if (selectSatus.value === 0) {
    return experimentStore.experiments;
  } else {
    return experimentStore.experiments.filter(item =>
      statusList.value[selectSatus.value].status.includes(item._status)
    );
  }
});

const change = index => {
  selectSatus.value = index;
  selectExperiment.value = "";
  experimentStore.setExperimentType(index);
  router.push("/dashboard")
};

const openExperiment = item => {
  selectExperiment.value = item.id;
  console.log(item);
  if (item._status == 0) {
    router.push({ path: "/result", query: { id: item.id, type: "Results", status: item._status } });
    return;
  }
  if (item._status <= -1 && item._status >= -8) {
    router.push({ path: "/result", query: { id: item.id, type: "Results", status: item._status } });
    return;
  }
  if (item._status == -9 || item._status > 0) {
    router.push({ path: "/setup", query: { id: item.id } });
  }
};
</script>
<style scoped lang="scss">
.my-experiment {
  padding: 24px 0;
  width: 214px;
  background: #fff;
  border-right: 1px solid #e0e0e0;
  height: 100%;

  .status-list {
    height: 25%;
    overflow: auto;
  }

  .header {
    padding: 0 20px;

    .title {
      font-size: 16px;
      font-weight: 600;
    }
  }

  .list {
    font-size: 14px;
    list-style: none;
    padding: 0;
    margin-top: 10px;
    position: relative;

    li {
      color: #525252;
      line-height: 32px;
      padding: 0 20px 0 35px;
      cursor: pointer;

      &.active {
        background: #8d8d8d33;
        box-shadow: 3px 0px 0px 0px #0f62fe inset;
      }
    }
  }

  .line {
    width: 182px;
    height: 1px;
    background: #c6c6c6;
    margin: 0 auto;
  }

  .experiment-list {
    margin-top: 10px;
    position: relative;
    height: 73%;
    overflow-y: auto;

    ul {
      li {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
  }
}
</style>
