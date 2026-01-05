<template>
  <template v-for="item in node" :key="item.id">
    <div class="block" v-if="item?.is_completed">
      <div>
        <CheckCircleFilled :style="{ color: item.is_completed ? '#0F62FE' : '#c6c6c6' }" class="icon" />
        <span class="title">{{ item.title }}</span>
      </div>
      <div class="description">{{ item.content }}</div>
    </div>
  </template>
</template>
<script setup>
import { ref, reactive } from "vue";
import { CheckCircleFilled } from "@ant-design/icons-vue";

const props = defineProps({
  node: {
    type: Array,
    required: true,
  },
});
</script>
<style lang="scss" scoped>
.block {
  width: 95%;
  margin: 0 auto 12px;
  background: #fff;
  padding: 15px;

  .icon {
    margin-right: 12px;
    font-size: 14px;
  }

  .title {
    font-size: 16px;
    color: #161616;
  }

  .description {
    margin-left: 30px;
    margin-top: 10px;
    // 超出10行省略号显示
    display: -webkit-box;
    -webkit-line-clamp: 10;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-word;
  }
}
</style>
