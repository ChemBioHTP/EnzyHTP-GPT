<template>
  <a-flex style="height: 100%;">
    <a-flex class="side" vertical justify="space-between" align="center">
      <div>
        <div @click="$router.push('/dashboard')">
          <img src="@/assets/img/application.png" alt="" class="icon" />
        </div>
        <div class="mt24" @click="$router.push('/dev')">
          <a-tooltip placement="right" title="Feature under development">
            <img src="@/assets/img/flow.png" alt="" class="icon" />
          </a-tooltip>
        </div>
      </div>
      <div>
        <div>
          <img src="@/assets/img/help.png" alt="" class="icon" />
        </div>
        <div class="mt24">
          <a-tooltip placement="right" title="Under Construction">
            <img src="@/assets/img/message.png" alt="" class="icon" />
          </a-tooltip>
        </div>
        <div class="mt24">
          <a-tooltip placement="right" title="Under Construction">
            <img src="@/assets/img/setting.png" alt="" class="icon" />
          </a-tooltip>
        </div>
      </div>
    </a-flex>
    <MyExperiment @change="change" @openExperiment="openExperiment" />
  </a-flex>
</template>
<script setup>
import MyExperiment from "@/components/MyExperiment.vue";
import { ref, reactive } from "vue";


const change = (data) => {
  // dataSource.value = data;
  
}

// const openExperiment = (experiment) => {
//   router.push({ path: '/setup', query: { id: experiment.id } });
// }

</script>
<style lang="scss" scoped>
.side {
  width: 48px;
  height: 100%;
  padding: 24px 0;
  background: #fff;
  border-right: 1px solid #e0e0e0;
}
</style>
