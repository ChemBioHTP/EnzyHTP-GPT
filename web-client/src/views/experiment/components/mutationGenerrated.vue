<template>
  <div>
    <a-flex justify="space-between">
      <div class="mutation-title">Mutation generated</div>
      <DownloadOutlined class="download-icon" @click="handleDownload"  v-if="showDownload"/>
      </a-flex>
    <a-row class="mutation-header">
      <a-col :span="8">Number</a-col>
      <a-col :span="16">Pattern</a-col>
    </a-row>
    <div class="mutation-list" v-if="mutations.length">
      <a-row v-for="(item, index) in mutations" class="item">
        <a-col :span="8">{{ index + 1 }}</a-col>
        <a-col :span="16">{{ item }}</a-col>
      </a-row>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive } from "vue";
import { DownloadOutlined } from "@ant-design/icons-vue";
const props = defineProps({
  mutations: {
    type: Array,
    default: () => [],
  },
  showDownload: {
    type: Boolean,
    default: false,
  },
});

const handleDownload = () => { 

};

</script>
<style lang="scss" scoped>
.mutation-title {
  color: #161616;
  font-size: 14px;
  font-weight: 600;
}
.download-icon{
  cursor: pointer;
  font-size: 16px;
}

.mutation-header {
  background: #e0e0e0;
  padding: 0 16px;
  margin-top: 20px;

  > div {
    color: #161616;
    font-size: 14px;
    font-weight: 600;
    line-height: 25px;
  }
}

.mutation-list {
  max-height: clamp(200px, 50vh, 1000px); // 随视口高度自适应
  overflow-y: auto;

  .item {
    background: #fff;
    border-top: 1px solid #dbdbdb;
    padding: 10px 16px;
    height: 50px;
    line-height: 30px;
  }
}
</style>
