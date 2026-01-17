<template>
  <a-modal v-model:open="showGUI" destroyOnClose @cancel="showGUI = false" title="Choose from GUI : atom indexes"
    :footer="null" :width="modalWidth" :bodyStyle="bodyStyle" wrapClassName="new-experiment-modal" @afterClose="reset">
    <a-flex v-if="showPdbSelect" class="pdb-select" align="center">
      <span class="label">Variant</span>
      <a-select
        v-model:value="selectedPdbExperimentId"
        :options="pdbSelectOptions"
        :loading="pdbFilesLoading"
        class="select"
        placeholder="Select a variant"
        @change="handlePdbChange"
      />
    </a-flex>
    <div :style="{ height: modalHeight + 'px', position: 'relative' }">
      <div id="viewer-container" width="100%" height="100%"></div>
      <!-- 拖拽小角 -->

      <ArrowsAltOutlined class="resizer" @mousedown="startResize" style="font-size: 40px;" />
    </div>
  </a-modal>
</template>
<script setup>
import { ref, onMounted, computed, shallowRef } from "vue";
import { ArrowsAltOutlined } from "@ant-design/icons-vue";
import { get_pdb_files } from "@/api/experiment";
const props = defineProps({
  experiment_id: {
    type: String,
    required: true,
  },
});

const modalWidth = ref(900)
const modalHeight = ref(600)
const pdbFiles = ref([])
const pdbFilesLoading = ref(false)
const selectedPdbExperimentId = ref("")
const viewerRef = shallowRef(null)

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

const showPdbSelect = computed(() => {
  return pdbFiles.value.length > 1
});

const pdbSelectOptions = computed(() => {
  return pdbFiles.value.map(item => {
    const label = item.pdb_filename ? `${item.name} (${item.pdb_filename})` : item.name;
    return { label, value: item.experiment_id };
  });
});

const buildPdbUrl = () => {
  const baseUrl = `/api/experiment/${props.experiment_id}/pdb_file`;
  if (selectedPdbExperimentId.value) {
    return `${baseUrl}?sub_experiment_id=${encodeURIComponent(selectedPdbExperimentId.value)}`;
  }
  return baseUrl;
};

const refreshStructure = async () => {
  console.log("[guiModal] refreshStructure: start", {
    hasViewer: !!viewerRef.value,
    hasPlugin: !!viewerRef.value?.plugin,
    hasClear: typeof viewerRef.value?.clear === "function",
    hasLoad: typeof viewerRef.value?.loadStructureFromUrl === "function",
    hasPluginLoad: typeof viewerRef.value?.plugin?.loadStructureFromUrl === "function",
  });
  const viewer = viewerRef.value;
  if (!viewer) {
    console.warn("[guiModal] refreshStructure: viewerRef is empty, abort");
    return;
  }
  if (viewer.plugin?.clear) {
    console.log("[guiModal] refreshStructure: clearing via plugin.clear()");
    await viewer.plugin.clear();
  } else if (typeof viewer.clear === "function") {
    console.log("[guiModal] refreshStructure: clearing via viewer.clear()");
    await viewer.clear();
  } else {
    console.log("[guiModal] refreshStructure: no clear method found");
  }
  const pdbUrl = buildPdbUrl();
  const loadFn = viewer.loadStructureFromUrl || viewer.plugin?.loadStructureFromUrl;
  const loadTarget = viewer.loadStructureFromUrl ? "viewer" : "plugin";
  console.log("[guiModal] refreshStructure: loadStructureFromUrl", {
    pdbUrl,
    hasLoadFn: typeof loadFn === "function",
    loadFnName: loadFn?.name,
    loadTarget,
    viewerKeys: Object.keys(viewer || {}),
    viewerCtor: viewer?.constructor?.name,
    pluginCtor: viewer?.plugin?.constructor?.name,
  });
  if (typeof loadFn !== "function") {
    console.error("[guiModal] refreshStructure: loadStructureFromUrl is not a function", {
      loadFn,
    });
    return;
  }
  try {
    const boundTarget = loadTarget === "viewer" ? viewer : viewer.plugin;
    await loadFn.call(boundTarget, pdbUrl, "pdb", false, {
      representationStyle: "cartoon",
    });
    console.log("[guiModal] refreshStructure: done");
  } catch (err) {
    console.error("[guiModal] refreshStructure: loadStructureFromUrl failed", err);
  }
};

const handlePdbChange = async () => {
  await refreshStructure();
};

const fetchPdbFiles = async () => {
  pdbFilesLoading.value = true;
  try {
    const res = await get_pdb_files(props.experiment_id);
    if (res?.is_successful) {
      pdbFiles.value = res.pdb_files || [];
      if (!selectedPdbExperimentId.value && pdbFiles.value.length) {
        selectedPdbExperimentId.value = pdbFiles.value[0].experiment_id;
      }
    }
  } finally {
    pdbFilesLoading.value = false;
  }
};

onMounted(() => {
  setTimeout(async () => {
    console.log("[guiModal] onMounted: start");
    console.log("[guiModal] onMounted: fetchPdbFiles()");
    await fetchPdbFiles();
    console.log("[guiModal] onMounted: fetchPdbFiles() done", {
      pdbFilesCount: pdbFiles.value.length,
      selectedPdbExperimentId: selectedPdbExperimentId.value,
    });
    console.log("[guiModal] onMounted: create molstar viewer");
    viewerRef.value = await molstar.Viewer.create("viewer-container", {
      layoutIsExpanded: false,
      // layoutShowControls: false,
      // layoutShowSequence: false,
      layoutShowLog: false,
      layoutShowToolbar: true, // 显示工具栏
      // layoutShowLeftPanel: false,
      collapseLeftPanel: true,
      // layoutShowParameters: false, // 是否显示参数面板
    });
    console.log("[guiModal] onMounted: molstar viewer created", {
      hasViewer: !!viewerRef.value,
      hasLoad: typeof viewerRef.value?.loadStructureFromUrl === "function",
      hasPluginLoad: typeof viewerRef.value?.plugin?.loadStructureFromUrl === "function",
      viewerCtor: viewerRef.value?.constructor?.name,
    });

    // 加载分子结构
    console.log("[guiModal] onMounted: refreshStructure()");
    await refreshStructure();
    console.log("[guiModal] onMounted: refreshStructure() done");
    console.log("[guiModal] onMounted: makeDraggable()");
    makeDraggable()
    console.log("[guiModal] onMounted: done");
  }, 500);
});
</script>
<style scoped>
.pdb-select {
  margin: 0 0 8px 0;
}

.pdb-select .label {
  margin-right: 8px;
  font-size: 14px;
  color: #161616;
}

.pdb-select .select {
  min-width: 260px;
}

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
