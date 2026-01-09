<template>
  <div class="box">
    <a-flex justify="space-between" align="center">
      <div class="title">Workflow</div>
      <img
        v-if="show"
        src="@/assets/img/eye.svg"
        alt=""
        @click="openWorkflow = true"
        class="icon"
      />
      <img
        v-else
        src="@/assets/img/edit.svg"
        alt=""
        @click="openWorkflow = true"
        class="icon"
      />
    </a-flex>
    <a-flex justify="space-between" class="width100">
      <a-flex
        v-for="(item, index) in list"
        :key="index"
        align="center"
        class="workflow-item"
      >
        <div :class="['item', item.disabled ? 'disabled' : '']">
          <div class="title">{{ item.title }}</div>
          <div class="description">
            {{ item.description }}
          </div>
        </div>
        <img
          src="@/assets/img/black_arrow.png"
          class="arrow"
          v-if="index < list.length - 1"
        />
      </a-flex>
    </a-flex>
  </div>
  <div class="box">
    <a-flex justify="space-between" align="center">
      <div>
        <span class="title">Target metrics</span>
        <span class="description ml50">
          {{ metrics.map(item => item.name).join(', ') }}  
        </span>
      </div>
      <img
        v-if="show"
        src="@/assets/img/eye.svg"
        alt=""
        @click="openMetrics = true"
        class="icon"
      />
      <img
        v-else
        src="@/assets/img/edit.svg"
        alt=""
        @click="openMetrics = true"
        class="icon"
      />
    </a-flex>
  </div>
  <div class="box">
    <a-flex justify="space-between" align="center">
      <div>
        <span class="title">Geometry constraint</span>
        <span class="description ml50">{{ constraintText }}</span>
      </div>
      <img v-if="show" src="@/assets/img/eye.svg" alt="" class="icon" />
      <img v-else src="@/assets/img/edit.svg" alt="" class="icon" />
    </a-flex>
  </div>
  <!-- ------------drawer---------------- -->
  <!-- workflow drawer -->
  <a-drawer
    v-model:open="openWorkflow"
    class="workflow-drawer"
    width="488"
    title="Change workflow"
    placement="right"
    @after-open-change="afterOpenChange"
  >
    <div class="position-relative">
      <p>
        Configure the workflow for your experiment below.
      </p>
      <a-form layout="vertical" class="mt24">
        <a-form-item label="Workflow">
          <a-select
            v-model:value="selectV"
            size="large"
            :options="options"
            style="width: 100%"
          ></a-select>
        </a-form-item>
      </a-form>
      <a-flex wrap="wrap">
        <div v-for="(item, index) in workFlowList" class="mt10">
          <span class="item">{{ item }}</span>
          <img
            src="@/assets/img/right-arrow.png"
            class="right-arrow"
            v-if="index < workFlowList.length - 1"
          />
        </div>
      </a-flex>
      <a-flex
        class="drawer-content mt60"
        justify="center"
        align="center"
        vertical
      >
        <img src="@/assets/img/workflow-drawer.svg" />
        <p class="description mt24">
          In the beta, only predefined workflows are offered. Custom workflows
          are coming in our next update. Stay tuned!
        </p>
      </a-flex>
      <a-flex class="btn-group">
        <div @click="openWorkflow = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="disabled"
          @click="handleCreate"
          class="btn"
        >
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>
  <!-- metrics drawer -->
  <a-drawer
    v-model:open="openMetrics"
    class="metrics-drawer"
    width="488"
    title="Select target metrics"
    placement="right"
    @after-open-change="afterOpenChange"
  >
    <div class="position-relative">
      <p>Choose the metrics you'd like to view following the experiment.</p>
      <div class="config">
        <a-flex
          align="center"
          v-for="(item, index) in metricsList"
          :class="['item', item.disabled ? 'disabled' : '']"
        >
          <div class="checkbox" @click="changeMetrics(item)">
            <img
              src="@/assets/img/checked.png"
              class="icon"
              v-if="item.checked"
            />
            <img src="@/assets/img/check.png" v-else class="icon" />
            {{ item.label }}
          </div>
          <span>{{ item.des }}</span>
          <img
            src="@/assets/img/edit.svg"
            @click="openEdit(item)"
            class="icon"
          />
        </a-flex>
      </div>
      <a-flex class="btn-group">
        <div @click="openMetrics = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="disabled"
          @click="saveMetrics"
          class="btn"
        >
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>
  <!-- constraint drawer -->
  <!-- <a-drawer v-model:open="openConstraint" class="custom-class" root-class-name="root-class-name" :root-style="{ }"
        title="Basic Drawer" placement="right" @after-open-change="afterOpenChange">
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
    </a-drawer> -->

  <!-- ------------config drawer--------------------- -->
  <!-- EF Config -->
  <a-drawer
    v-model:open="model.openEF"
    class="custom-class"
    width="488"
    title="Adding inputs for EF"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected (EF) needs further details. Please provide the
        following inputs.
      </p>
      <div class="config mt40">
        <p class="title">Index of bond atoms</p>
        <p class="description">
          Specify the atom indexes that defines the bond of interest.
        </p>
        <a-flex gap="middle">
          <a-input size="large" placeholder="e.g. 1,2,3,4" />
          <a-input size="large" placeholder="e.g. 1,2,3,4" />
        </a-flex>
      </div>
      <a-flex class="btn-group">
        <div @click="model.openEF = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="disabled"
          @click="handleCreate"
          class="btn"
        >
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>

  <!-- SPI Config -->
  <a-drawer
    v-model:open="model.openSPI"
    class="custom-class"
    width="488"
    title="Adding inputs for SPI"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected needs further details. Please provide the
        following inputs.
      </p>
      <div class="config mt40">
        <p class="title">Substrate</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="spiModel.ligand"
        />
      </div>
      <div class="config mt40">
        <p class="title">Pocket</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="spiModel.region_pattern"
        />
      </div>
      <div class="config mt40">
        <p class="title">Protein</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="spiModel.Protein"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="model.openSPI = false" class="btn">Cancel</div>
        <a-button type="primary" size="large" @click="saveSpi" class="btn">
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>

  <!-- RMSD Config -->
  <a-drawer
    v-model:open="model.openRMSD"
    class="custom-class"
    width="488"
    title="Adding inputs for RMSD"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected needs further details. Please provide the
        following inputs.
      </p>
      <div class="config mt40">
        <p class="title">Pocket</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="RMSDModel.region_pattern"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="model.openRMSD = false" class="btn">Cancel</div>
        <a-button type="primary" size="large" @click="saveRMSD" class="btn">
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>

  <!-- MMPBSA Config -->
  <a-drawer
    v-model:open="model.openMMPBSA"
    class="custom-class"
    width="488"
    title="Adding inputs for MMPBSA"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected needs further details. Please provide the
        following inputs.
      </p>
      <div class="config mt40">
        <p class="title">Substrate</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="MMPBSAModel.ligand"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="model.openMMPBSA = false" class="btn">Cancel</div>
        <a-button type="primary" size="large" @click="saveMMPBSA" class="btn">
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>
</template>
<script setup>
import { ref, reactive, watch, computed } from "vue";
import { updateExperimentProfile } from "@/api/experiment";
import { useRoute } from "vue-router";
const route = useRoute();

const props = defineProps({
  metrics: {
    type: Array,
    default: () => [],
  },
  show: {
    type: Boolean,
    default: false,
  },
  constraints: {
    type: Array,
    default: () => [],
  },
});

const openMetrics = ref(false);
const openWorkflow = ref(false);

const model = reactive({
  openEF: false,
  openSPI: false,
  openRMSD: false,
  openMMPBSA: false,
});

const options = [{ label: "Predefined", value: "1" }];
const selectV = ref("1");

const spiModel = reactive({
  ligand: "",
  region_pattern: "",
  Protein: "",
});

const RMSDModel = reactive({
  region_pattern: "",
});

const MMPBSAModel = reactive({
  ligand: "",
});

const list = ref([
  {
    title: "Structure preparation",
    description: "Remove water, Protonation.",
  },
  {
    title: "Structure operation",
    description: "Mutation. Mutation-perturbed-protonation.",
  },
  { title: "Conformational Sampling", description: "Parameterization, MD simulation." },
  { title: "Metrics calculation", description: "Target metrics (See below)", disabled: false },
]);

const constraintText = computed(() => {
  if (!Array.isArray(props.constraints) || !props.constraints.length) {
    return "No constraint";
  }

  return props.constraints
    .map(item => {
      if (!item) return "";
      const type = item.type ? String(item.type) : "constraint";
      const args = item.arguments;
      if (Array.isArray(args) && args.length) {
        return `${type}: ${args.join(", ")}`;
      }
      if (args) {
        return `${type}: ${args}`;
      }
      return type;
    })
    .filter(Boolean)
    .join("; ");
});

const workFlowList = ref([
  "Remove water",
  "Protonation",
  "Mutation",
  "Mutation-perturbed-protonation",
  "Parameterization",
  "MD simulation",
  "Calculate metrics",
]);

const metricsList = ref([
  {
    label: "EF",
    checked: false,
    des: "",
    disabled: false,
    data: {
      name: "electric_field",
    },
  },
  {
    label: "SPI",
    checked: false,
    des: "pocket: default, substrate: default ",
    data: {
      name: "spi",
      arguments: {
        ligand: "",
        region_pattern: "",
        Protein: "",
      },
    },
  },
  {
    label: "RMSD/Stability",
    checked: false,
    data: {
      name: "active_site_rmsd",
      arguments: {
        region_pattern: "",
      },
    },
  },
  {
    label: "MMPBSA",
    checked: false,
    des: "ligand: default",
    data: {
      name: "mmpbgbsa",
      arguments: {
        ligand: "",
      },
    },
  },
]);

watch(
  () => props.metrics,
  () => {
    if (props.metrics.length) {
      console.log(props.metrics);
      props.metrics.map(item => {
        let metric = metricsList.value.find(m => m.data.name === item.name);
        if (metric) {
          metric.checked = true;
          Object.assign(metric.data.arguments, item.arguments);
        }
      });
      console.log(metricsList.value);
    }
  }
);

const openEdit = data => {
  if (data.label === "EF") {
    model.openEF = true;
  } else if (data.label === "SPI") {
    model.openSPI = true;
    Object.assign(spiModel, data.data.arguments);
  } else if (data.label === "RMSD/Stability") {
    model.openRMSD = true;
    Object.assign(RMSDModel, data.data.arguments);
  } else if (data.label === "MMPBSA") {
    model.openMMPBSA = true;
    Object.assign(MMPBSAModel, data.data.arguments);
  }
};

const changeMetrics = item => {
  if (item.disabled) return;
  item.checked = !item.checked;
};

const saveSpi = () => {
  let SPI = metricsList.value.find(item => item.label === "SPI");
  SPI.data.arguments = Object.assign({}, spiModel);
  model.openSPI = false;
};

const saveRMSD = () => {
  let RMSD = metricsList.value.find(item => item.label === "RMSD/Stability");
  RMSD.data.arguments = Object.assign({}, RMSDModel);
  model.openRMSD = false;
};

const saveMMPBSA = () => {
  let MMPBSA = metricsList.value.find(item => item.label === "MMPBSA");
  MMPBSA.data.arguments = Object.assign({}, MMPBSAModel);
  model.openMMPBSA = false;
};

const saveMetrics = () => {
  let list = metricsList.value.filter(item => item.checked);
  let formsData = new FormData();
  formsData.append("metrics", JSON.stringify(list.map(item => item.data)));

  console.log(metricsList.value);

  updateExperimentProfile(route.query.id, formsData).then(res => {
    console.log(res, metricsList.value);
    openMetrics.value = false;
  });
};
</script>
<style lang="scss" scoped>
.box {
  padding: 15px;
  border: 1px solid #e0e0e0;
  margin-bottom: 15px;
  border-radius: 5px;
  width: 100%;

  .workflow-item {
    // position: relative;
    flex: 1;
    &:last-child{
      flex: 0;
    }
  }
  .title {
    color: #000;
    font-size: 14px;
    font-weight: 600;
  }

  .item {
    width: 150px;
    height: 160px;
    background: #e7f1ff;
    border-radius: 3px;
    padding: 15px;
    margin-top: 15px;
    flex-shrink: 0;

    .title {
      color: #161616;
      font-size: 16px;
      font-weight: 400;
      margin-bottom: 15px;
    }

    .description {
      line-height: 20px;
    }
  }

  .arrow {
    width: 31px;
    height: 8px;
    margin-left:calc((100% - 180px) / 2 )
    // : 10%;
    // position: absolute;
    // right: -30%;
  }

  .description {
    color: #525252;
    font-size: 12px;
  }
}

.position-relative {
  position: relative;
  height: 97.6%;
}

.workflow-drawer {
  .item {
    // height: 16px;
    padding: 2px 8px;
    font-size: 12px;
    line-height: 16px;
    color: #161616;
    background: #e0e0e0;
    border-radius: 23px;
    margin: 0 4px;
    position: relative;
  }

  .right-arrow {
    display: inline-block;
    width: 12px;
    height: 6px;
  }

  .description {
    font-size: 14px;
    color: #525252;
    margin-top: 15px;
  }
}

.metrics-drawer {
  .config {
    .item {
      border: 1px solid #c6c6c6;
      padding: 8px 16px;
      border-radius: 3px;
      font-size: 16px;
      color: #161616;
      margin-bottom: 10px;
      gap: 10px;

      &.disabled .checkbox,
      &.disabled img {
        cursor: not-allowed;
        opacity: 0.5;
      }

      .checkbox {
        width: 160px;
        vertical-align: 1px;
        cursor: pointer;

        img {
          vertical-align: -2px;
        }
      }

      span {
        font-size: 12px;
        color: #525252;
        text-align: left;
        width: 70%;
      }
    }
  }
}

.custom-class {
  .config {
    padding: 0 15px;

    .title {
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 10px;

      color: #525252;
    }

    .description {
      font-size: 14px;
      color: #525252;
      margin-bottom: 15px;
    }
  }
}
</style>
