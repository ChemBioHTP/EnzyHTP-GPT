<template>
  <a-modal v-model:open="showGUI" destroyOnClose @cancel="showGUI = false" title="Choose from GUI : atom indexes"
    :footer="null" width="50%" :bodyStyle="bodyStyle" wrapClassName="new-experiment-modal">
    <div style="width: 100%; height: 400px; overflow: hidden; position: relative">
      <div id="viewer-container" width="100%" height="100px"></div>
    </div>
  </a-modal>
</template>
<script setup>
import { onMounted } from "vue";

const props = defineProps({
  experiment_id: {
    type: String,
    required: true,
  },
});
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
  }, 500);
});
</script>
<style scoped></style>
