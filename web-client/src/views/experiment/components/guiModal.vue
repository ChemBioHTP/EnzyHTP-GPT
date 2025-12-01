<template>
  <a-modal v-model:open="showGUI" destroyOnClose @cancel="showGUI = false" title="Choose from GUI : atom indexes"
    :footer="null" :width="modalWidth" :bodyStyle="bodyStyle" wrapClassName="new-experiment-modal" @afterClose="reset">
    <div :style="{ height: modalHeight + 'px', position: 'relative' }">
      <div id="viewer-container" width="100%" height="100%"></div>
      <!-- 拖拽小角 -->

      <ArrowsAltOutlined class="resizer" @mousedown="startResize" style="font-size: 40px;" />
    </div>
  </a-modal>
</template>
<script setup>
import { ref, onMounted, h } from "vue";
import { ArrowsAltOutlined } from "@ant-design/icons-vue";
const props = defineProps({
  experiment_id: {
    type: String,
    required: true,
  },
});

const modalWidth = ref(900)
const modalHeight = ref(600)

let startX = 0
let startY = 0
let startWidth = 0
let startHeight = 0

const startResize = (e) => {
  startX = e.clientX
  startY = e.clientY
  startWidth = modalWidth.value
  startHeight = modalHeight.value

  document.addEventListener('mousemove', resize)
  document.addEventListener('mouseup', stopResize)
}

const resize = (e) => {
  const dx = e.clientX - startX
  const dy = e.clientY - startY
  modalWidth.value = Math.max(300, startWidth + dx)
  modalHeight.value = Math.max(200, startHeight + dy)
}

const stopResize = () => {
  document.removeEventListener('mousemove', resize)
  document.removeEventListener('mouseup', stopResize)
}

// 拖动逻辑
const makeDraggable = () => {
  const modalHeader = document.querySelector('.new-experiment-modal .ant-modal-header')
  const modal = document.querySelector('.new-experiment-modal .ant-modal')
  console.log(modalHeader, modal)
  if (!modalHeader || !modal) return

  let isDragging = false
  let offsetX = 0
  let offsetY = 0

  modalHeader.style.cursor = 'move'

  modalHeader.onmousedown = (e) => {
    isDragging = true
    offsetX = e.clientX - modal.offsetLeft
    offsetY = e.clientY - modal.offsetTop
    document.onmousemove = (e) => {
      if (isDragging) {
        modal.style.margin = 0
        modal.style.left = e.clientX - offsetX + 'px'
        modal.style.top = e.clientY - offsetY + 'px'
        modal.style.position = 'absolute'
      }
    }
    document.onmouseup = () => {
      isDragging = false
      document.onmousemove = null
      document.onmouseup = null
    }
  }
}

const reset = () => {
  modalWidth.value = 600
  modalHeight.value = 400
}

const showGUI = defineModel();
onMounted(() => {
  setTimeout(async () => {
    const viewer = await molstar.Viewer.create("viewer-container", {
      layoutIsExpanded: false,
      layoutShowControls: false,
      layoutShowSequence: false,
      layoutShowLog: false,
      layoutShowToolbar: true, // 显示工具栏
      layoutShowLeftPanel: false,
      layoutShowStructure: false, // 是否显示结构面板
      layoutShowParameters: false, // 是否显示参数面板
    });

    // 加载分子结构
    await viewer.loadStructureFromUrl(
      `/api/experiment/${props.experiment_id}/pdb_file`,
      "pdb",
      false,
      {
        representationStyle: "cartoon",
      }
    );
    makeDraggable()
  }, 500);
});
</script>
<style scoped>
.resizer {
  position: absolute;
  width: 15px;
  height: 15px;
  right: 2px;
  bottom: 2px;
  cursor: se-resize;
  background: transparent;
  z-index: 10;
  transform: rotate(90deg);
}
</style>
