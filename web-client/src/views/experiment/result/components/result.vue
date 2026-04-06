<template>
  <a-flex class="result-container" justify="space-between">
    <div v-if="$route.query.status == '0'" class="result-wrap">
      <a-spin :spinning="spinning" class="result-spin">
        <h3>Summary</h3>
        <div class="result-content mt15">
          <div class="summary-wrap">
            <div
              v-if="resultData.result_interpretation"
              class="interpretation"
              v-html="formattedText(resultData.result_interpretation)"
            ></div>
            <div v-else class="interpretation-placeholder">
              <div v-if="isInterpretationPending" class="interpretation-loading">
                <a-spin size="large" />
                <div class="loading-text">{{ interpretationMessage }}</div>
              </div>
              <div v-else>{{ interpretationMessage }}</div>
            </div>
          </div>
          <div v-if="imageItems.length" class="curve-panel">
            <div class="curve-header">
              <div class="curve-title">Equilibration Curves</div>
              <div class="curve-actions">
                <a-button
                  type="link"
                  size="small"
                  class="curve-action-btn"
                  :loading="loadingAllImages"
                  @click="handleToggleImages"
                >
                  {{ showingAllImages ? "Collapse Preview" : "Show All" }}
                </a-button>
              </div>
            </div>
            <div class="curve-scroll">
              <div
                v-for="(item, index) in imageItems"
                :key="`${index}-${item.filename || ''}`"
                class="result-img-wrap"
              >
                <div class="result-img-title">{{ item.title || "Equilibration Curve" }}</div>
                <img :src="item.src || item" alt="" class="result-img">
              </div>
            </div>
          </div>
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
import { computed, onUnmounted, ref } from "vue";
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
const PREVIEW_IMAGE_COUNT = 6
const INTERPRETATION_POLL_INTERVAL_MS = 5000
const MAX_INTERPRETATION_POLL_ATTEMPTS = 72
const previewImageItems = ref([])
const allImageItems = ref([])
const showingAllImages = ref(false)
const loadingAllImages = ref(false)
let interpretationPollTimer = null

const interpretationMessage = computed(() => {
  if (resultData.value?.result_interpretation) {
    return ""
  }
  return (
    resultData.value?.result_interpretation_message
    || "Result interpretation is being generated. Please wait a moment."
  )
})
const isInterpretationPending = computed(() => {
  return resultData.value?.result_interpretation_status === "pending"
})
const imageItems = computed(() => {
  if (showingAllImages.value && allImageItems.value.length) {
    return allImageItems.value
  }
  if (previewImageItems.value.length) {
    return previewImageItems.value
  }
  const items = resultData.value?.result_image_items
  if (Array.isArray(items) && items.length) {
    return items
  }
  const fallback = resultData.value?.result_images
  if (Array.isArray(fallback) && fallback.length) {
    return fallback.map((src, index) => ({
      src,
      title: `Equilibration Curve ${index + 1}`,
      filename: "",
    }))
  }
  return []
})

const normalizeImageItems = payload => {
  const items = payload?.result_image_items
  if (Array.isArray(items) && items.length) {
    return items
  }
  const fallback = payload?.result_images
  if (Array.isArray(fallback) && fallback.length) {
    return fallback.map((src, index) => ({
      src,
      title: `Equilibration Curve ${index + 1}`,
      filename: "",
    }))
  }
  return []
}

const formattedText = text => {
  if (!text) return "";
  return marked.parse(text);
};
// 安全地解析包含 NaN 的 JSON-like 字符串
const safeParseWithNaN = (str) => {
  try {
    return new Function(`return (${str})`)();
  } catch (e) {
    return str;
  }
};
const fetchResult = imageLimit => {
  return getExperimentResult(route.query.id, { image_limit: imageLimit }).then(res => {
    if (!res) {
      return null
    }
    const result = typeof res === "string" ? safeParseWithNaN(res) : res
    if (result && result.is_authenticated) {
      return result
    }
    return null
  })
}

const stopInterpretationPolling = () => {
  if (interpretationPollTimer) {
    clearTimeout(interpretationPollTimer)
    interpretationPollTimer = null
  }
}

const shouldContinueInterpretationPolling = payload => {
  if (!payload) {
    return true
  }
  if (payload.result_interpretation) {
    return false
  }
  const status = payload.result_interpretation_status
  if (status === "pending") {
    return true
  }
  return false
}

const scheduleInterpretationPolling = (attempt = 0) => {
  if (attempt >= MAX_INTERPRETATION_POLL_ATTEMPTS) {
    stopInterpretationPolling()
    return
  }
  stopInterpretationPolling()
  interpretationPollTimer = setTimeout(() => {
    fetchResult(PREVIEW_IMAGE_COUNT)
      .then(result => {
        if (result) {
          resultData.value = result
          previewImageItems.value = normalizeImageItems(result)
        }
        if (shouldContinueInterpretationPolling(result)) {
          scheduleInterpretationPolling(attempt + 1)
        } else {
          stopInterpretationPolling()
        }
      })
      .catch(() => {
        scheduleInterpretationPolling(attempt + 1)
      })
  }, INTERPRETATION_POLL_INTERVAL_MS)
}

const handleToggleImages = () => {
  if (showingAllImages.value) {
    showingAllImages.value = false
    return
  }
  if (allImageItems.value.length) {
    showingAllImages.value = true
    return
  }
  loadingAllImages.value = true
  fetchResult(0)
    .then(result => {
      if (!result) {
        return
      }
      allImageItems.value = normalizeImageItems(result)
      showingAllImages.value = true
    })
    .finally(() => {
      loadingAllImages.value = false
    })
}

if (route.query.status == '0') {
  spinning.value = true;
  fetchResult(PREVIEW_IMAGE_COUNT)
    .then(result => {
      if (result) {
        resultData.value = result
        previewImageItems.value = normalizeImageItems(result)
        if (shouldContinueInterpretationPolling(result)) {
          scheduleInterpretationPolling(0)
        }
      }
    })
    .finally(() => {
      spinning.value = false;
    })
}

onUnmounted(() => {
  stopInterpretationPolling()
})
</script>
<style lang="scss" scoped>
.result-container {
  // margin: 60px 70px;
  height: 65vh;
  width: 100%;
  padding: 0 32px;
  min-height: 0;
  overflow: hidden;

  .list {
    width: 420px;
    border-left: 1px solid #e0e0e0;
    padding: 30px 17px;
    margin-left: 15px;
    height: 60vh;
    overflow: auto;
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
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .result-spin {
    height: 100%;
    min-height: 0;
    overflow: hidden;
  }

  :deep(.ant-spin-nested-loading) {
    height: 100%;
    min-height: 0;
    overflow: hidden;
  }

  :deep(.ant-spin-container) {
    height: 100%;
    display: flex;
    flex-direction: column;
    min-height: 0;
    overflow: hidden;
  }

  .result-content {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 15px;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 2px;
  }

  .summary-wrap {
    border: 1px solid #e9e9e9;
    border-radius: 8px;
    padding: 16px 18px;
    background: #fff;
    flex: none;
  }

  .interpretation-placeholder {
    color: #595959;
    min-height: 64px;
    line-height: 1.6;
    white-space: pre-wrap;
  }

  .interpretation-loading {
    min-height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }

  .loading-text {
    text-align: center;
    line-height: 1.5;
  }

  .result-img {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 6px;
  }

  .curve-panel {
    width: 100%;
    border: 1px solid #e9e9e9;
    border-radius: 8px;
    background: #fff;
    padding: 12px 14px;
    flex-shrink: 0;
  }

  .curve-scroll {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    max-height: none;
    overflow: visible;
  }

  .result-img-wrap {
    width: 48%;
  }

  .result-img-title {
    font-size: 12px;
    color: #595959;
    line-height: 1.4;
    margin-bottom: 6px;
    word-break: break-word;
  }

  .curve-title {
    font-size: 16px;
    font-weight: 600;
  }

  .curve-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }

  .curve-actions {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
  }

  .curve-action-btn {
    padding: 0 4px;
  }

  .interpretation {
    font-size: 16px;
    color: #000;
    line-height: 140%;
  }
}

.mt15 {
  margin-top: 15px;
}
</style>
