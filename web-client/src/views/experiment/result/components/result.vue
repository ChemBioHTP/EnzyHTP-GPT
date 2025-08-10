<template>
  <a-flex class="result-container" justify="space-between">
    <div v-if="$route.query.status == '0'" class="result-wrap">
      <a-spin :spinning="spinning">
        <h3>Summary</h3>
        <div class="flex-wrap mt15 img-wrap">
          <img :src="item" alt="" v-for="(item, index) in resultData.result_images" class="result-img">
          <img :src="item" alt="" v-for="(item, index) in resultData.result_images" class="result-img">
          <img :src="item" alt="" v-for="(item, index) in resultData.result_images" class="result-img">
          <img :src="item" alt="" v-for="(item, index) in resultData.result_images" class="result-img">

        </div>
        <div class="interpretation">
          <p v-html="formattedText(resultData.result_interpretation)"></p>
        </div>
      </a-spin>
    </div>
    <div class="process-wrap" v-else>
      <img src="@/assets/img/results-icon.png" class="process-icon" />
      <div class="title mt40">MD simulation in progress</div>
      <div class="description">
        Your target metrics will be visible once the process is done.
      </div>
      <a-progress :percent="progress" status="active" class="mt10" />
      <div></div>
    </div>
    <div class="list">
      <FileList :list="resultData.downloadable_files" />
      <MutationGenerrated :mutations="mutations" :showDownload="true" style="margin-top: 68px;" />
    </div>
  </a-flex>
</template>
<script setup>
import { ref, reactive } from "vue";
import MutationGenerrated from "@/views/experiment/components/mutationGenerrated.vue";
import FileList from "@/views/experiment/components/fileList.vue";
import { getExperimentResult } from "@/api/experiment";
import { useRoute } from "vue-router";
let route = useRoute();
const props = defineProps({
  progress: {
    type: Number,
    default: 0,
  },
  mutations: {
    type: Array,
    default: () => [],
  },
});
const spinning = ref(false);
const resultData = ref({})

const formattedText = text => {
  if (!text) return "";
  return marked.parse(text);
};
// 安全地解析包含 NaN 的 JSON-like 字符串
const safeParseWithNaN = (str) => {
  try {
    return new Function(`return (${str})`)();
  } catch (e) {
    console.error("解析失败:", e);
    return null;
  }
};
if (route.query.status == '0') {
  spinning.value = true;
  getExperimentResult(route.query.id).then(res => {
    spinning.value = false;
    if (res) {
      let result = safeParseWithNaN(res)
      console.log(result);
      if (result && result.is_successful && result.is_authenticated) {
        resultData.value = result
      }
    }
  })
}
</script>
<style lang="scss" scoped>
.result-container {
  // margin: 60px 70px;
  height: 65vh;
  width: 100%;
  padding: 0 32px;

  .list {
    width: 420px;
    border-left: 1px solid #e0e0e0;
    padding: 30px 17px;
    margin-left: 15px;
  }
}

.process-wrap {
  width: 580px;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;

  .process-icon {
    width: 159px;
    height: 190px;
  }

  .title {
    color: #161616;
    font-weight: 600;
    font-size: 20px;
  }

  .description {
    color: #595959;
    font-size: 16px;
    margin-top: 15px;
  }
}

.result-wrap {
  width: 100%;
  height: 100%;
  max-width: 1000px;

  .img-wrap {
    display: flex;
    flex-wrap: wrap;
    /* 允许换行 */
    gap: 10px;
    /* 设置图片之间的间隔 */
    height: 300px;
    overflow: auto;
  }

  .result-img {
    width: 48%;
    /* 每个图片宽度为父容器的 48%，两个图片并排 */
    height: auto;
    /* 保持图片的等比例显示 */
    object-fit: cover;
    /* 确保图片不变形 */
  }

  .interpretation {
    font-size: 16px;
    color: #000;
    margin-top: 40px;
    line-height: 140%;
    max-height: 400px;
    overflow: auto;
  }
}

.mt15 {
  margin-top: 15px;
}
</style>
