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
      <img
        v-else
        src="@/assets/img/edit.svg"
        alt=""
        class="icon"
        @click="openConstraint = true"
      />
    </a-flex>
  </div>
  <div class="box">
    <a-flex justify="space-between" align="center">
      <div>
        <span class="title">MD simulation duration</span>
        <span class="description ml50">{{ mdLengthDisplay }}</span>
      </div>
      <img v-if="show" src="@/assets/img/eye.svg" alt="" class="icon" />
      <img
        v-else
        src="@/assets/img/edit.svg"
        alt=""
        @click="openMdLength = true"
        class="icon"
      />
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
  <!-- md length drawer -->
  <a-drawer
    v-model:open="openMdLength"
    class="custom-class"
    width="488"
    title="Adjust MD simulation duration"
    placement="right"
  >
    <div class="position-relative">
      <p>Set the length of the MD simulation in nanoseconds.</p>
      <div class="config mt40">
        <p class="title">MD simulation duration (ns)</p>
        <p class="description">Enter a positive value in nanoseconds.</p>
        <a-input
          size="large"
          type="number"
          min="0"
          step="0.01"
          placeholder="e.g. 50"
          v-model:value="mdLengthInput"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="openMdLength = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="mdLengthSaving"
          @click="saveMdLength"
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
  <a-drawer
    v-model:open="openConstraint"
    class="constraints-drawer"
    width="488"
    title="Edit geometry constraints"
    placement="right"
  >
    <div class="position-relative">
      <p>Define constraints using atom selections (e.g. A.101.OE2).</p>
      <div class="constraint-list mt24">
        <div
          v-for="(constraint, index) in constraintsModel"
          :key="constraint.id"
          class="constraint-row"
        >
          <div class="row-head">
            <a-select
              v-model:value="constraint.type"
              size="large"
              :options="constraintTypeOptions"
              style="width: 160px"
              @change="handleConstraintTypeChange(constraint)"
            />
            <div class="row-actions">
              <img
                src="@/assets/img/del.svg"
                class="icon"
                @click="removeConstraint(index)"
              />
            </div>
          </div>
          <a-flex class="row-body" gap="middle">
            <a-input
              v-for="argIndex in getConstraintArgCount(constraint.type)"
              :key="argIndex"
              size="large"
              :placeholder="`Atom ${argIndex}`"
              v-model:value="constraint.arguments[argIndex - 1]"
            />
          </a-flex>
        </div>
      </div>
      <div class="add-constraint" @click="addConstraint">
        + Add constraint
      </div>
      <a-flex class="btn-group">
        <div @click="openConstraint = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="constraintsSaving"
          @click="saveConstraints"
          class="btn"
        >
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>

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
          <a-input
            size="large"
            placeholder="e.g. A.254.C1"
            v-model:value="efModel.atom_1"
          />
          <a-input
            size="large"
            placeholder="e.g. A.253.S1"
            v-model:value="efModel.atom_2"
          />
        </a-flex>
      </div>
      <a-flex class="btn-group">
        <div @click="model.openEF = false" class="btn">Cancel</div>
        <a-button
          type="primary"
          size="large"
          :disabled="disabled"
          @click="saveEF"
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

  <!-- Cavity Config -->
  <a-drawer
    v-model:open="model.openCavity"
    class="custom-class"
    width="488"
    title="Adding inputs for Cavity volume"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected needs further details. Provide either a ligand
        or a pocket residue pattern.
      </p>
      <div class="config mt40">
        <p class="title">Ligand selection pattern</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="cavityModel.ligand_selection_pattern"
        />
      </div>
      <div class="config mt40">
        <p class="title">Pocket residue pattern</p>
        <p class="description">A selection pattern defined in PyMol style.</p>
        <a-input
          size="large"
          placeholder="string"
          v-model:value="cavityModel.pocket_compositing_residue_pattern"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="model.openCavity = false" class="btn">Cancel</div>
        <a-button type="primary" size="large" @click="saveCavity" class="btn">
          <a-flex class="button-content" justify="space-between" align="center">
            <span>Save</span>
          </a-flex>
        </a-button>
      </a-flex>
    </div>
  </a-drawer>

  <!-- DSI Config -->
  <a-drawer
    v-model:open="model.openDSI"
    class="custom-class"
    width="488"
    title="Adding inputs for DSI"
    placement="right"
  >
    <div class="position-relative">
      <p>
        The metric you selected needs further details. Please provide the
        domain sequences.
      </p>
      <div class="config mt40">
        <p class="title">Domain 1 sequence</p>
        <p class="description">Amino acid sequence for the first domain.</p>
        <a-input
          size="large"
          placeholder="sequence"
          v-model:value="dsiModel.domain1_sequence"
        />
      </div>
      <div class="config mt40">
        <p class="title">Domain 2 sequence</p>
        <p class="description">Amino acid sequence for the second domain.</p>
        <a-input
          size="large"
          placeholder="sequence"
          v-model:value="dsiModel.domain2_sequence"
        />
      </div>
      <a-flex class="btn-group">
        <div @click="model.openDSI = false" class="btn">Cancel</div>
        <a-button type="primary" size="large" @click="saveDSI" class="btn">
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
import { message } from "ant-design-vue";
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
  mdLength: {
    type: [Number, String],
    default: null,
  },
});

const openMetrics = ref(false);
const openWorkflow = ref(false);
const openMdLength = ref(false);
const openConstraint = ref(false);
const mdLengthValue = ref("");
const mdLengthInput = ref("");
const mdLengthSaving = ref(false);
const constraintsSaving = ref(false);

const model = reactive({
  openEF: false,
  openSPI: false,
  openRMSD: false,
  openMMPBSA: false,
  openCavity: false,
  openDSI: false,
});

const options = [{ label: "Predefined", value: "1" }];
const selectV = ref("1");

const spiModel = reactive({
  ligand: "",
  region_pattern: "",
  Protein: "",
});

const efModel = reactive({
  atom_1: "",
  atom_2: "",
});

const RMSDModel = reactive({
  region_pattern: "",
});

const MMPBSAModel = reactive({
  ligand: "",
});

const cavityModel = reactive({
  ligand_selection_pattern: "",
  pocket_compositing_residue_pattern: "",
});

const dsiModel = reactive({
  domain1_sequence: "",
  domain2_sequence: "",
});

const constraintTypeOptions = [
  { label: "Distance", value: "distance" },
  { label: "Angle", value: "angle" },
  { label: "Dihedral", value: "dihedral" },
];

const constraintsModel = ref([]);

const constraintArgCounts = {
  distance: 2,
  angle: 3,
  dihedral: 4,
};

const getConstraintArgCount = type => {
  return constraintArgCounts[type] || constraintArgCounts.distance;
};

const normalizeConstraintRow = row => {
  const count = getConstraintArgCount(row.type);
  if (!Array.isArray(row.arguments)) {
    row.arguments = [];
  }
  for (let i = 0; i < count; i += 1) {
    if (row.arguments[i] === undefined || row.arguments[i] === null) {
      row.arguments[i] = "";
    }
  }
  if (row.arguments.length > count) {
    row.arguments = row.arguments.slice(0, count);
  }
  return row;
};

const buildConstraintRow = (constraint = {}) => {
  const type = constraint.type || "distance";
  const args = Array.isArray(constraint.arguments) ? [...constraint.arguments] : [];
  return normalizeConstraintRow({
    id: `${Date.now()}-${Math.random()}`,
    type,
    arguments: args,
  });
};

const loadConstraintsFromProps = () => {
  if (Array.isArray(props.constraints) && props.constraints.length) {
    constraintsModel.value = props.constraints.map(item =>
      buildConstraintRow(item || {})
    );
  } else {
    constraintsModel.value = [buildConstraintRow()];
  }
};

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

const mdLengthDisplay = computed(() => {
  if (mdLengthValue.value === "" || mdLengthValue.value === null || mdLengthValue.value === undefined) {
    return "Not set";
  }
  return `${mdLengthValue.value} ns`;
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
      arguments: {
        atom_1: "",
        atom_2: "",
      },
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
    label: "RMSD",
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
  {
    label: "DDG Fold",
    checked: false,
    des: "Relative folding free energy.",
    data: {
      name: "ddg_fold",
      arguments: {},
    },
  },
  {
    label: "Cavity Volume",
    checked: false,
    des: "Ligand/pocket cavity volume.",
    data: {
      name: "cavity",
      arguments: {
        ligand_selection_pattern: "",
        pocket_compositing_residue_pattern: "",
      },
    },
  },
  {
    label: "DSI",
    checked: false,
    des: "Domain separation index.",
    data: {
      name: "dsi",
      arguments: {
        domain1_sequence: "",
        domain2_sequence: "",
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

watch(
  () => props.mdLength,
  value => {
    if (value === null || value === undefined || value === "") {
      mdLengthValue.value = "";
      mdLengthInput.value = "";
      return;
    }
    mdLengthValue.value = value;
    mdLengthInput.value = String(value);
  },
  { immediate: true }
);

watch(openMdLength, value => {
  if (value) {
    mdLengthInput.value =
      mdLengthValue.value === "" || mdLengthValue.value === null || mdLengthValue.value === undefined
        ? ""
        : String(mdLengthValue.value);
  }
});

watch(
  () => props.constraints,
  () => {
    if (!openConstraint.value) {
      loadConstraintsFromProps();
    }
  },
  { deep: true }
);

watch(openConstraint, value => {
  if (value) {
    loadConstraintsFromProps();
  }
});

const pickMetricValue = (args, keys, fallback = "") => {
  if (!args) return fallback;
  for (const key of keys) {
    if (args[key] !== undefined && args[key] !== null && args[key] !== "") {
      return args[key];
    }
  }
  return fallback;
};

const openEdit = data => {
  const args = data?.data?.arguments || {};
  if (data.label === "EF") {
    model.openEF = true;
    efModel.atom_1 = pickMetricValue(args, ["atom_1"]);
    efModel.atom_2 = pickMetricValue(args, ["atom_2"]);
  } else if (data.label === "SPI") {
    model.openSPI = true;
    spiModel.ligand = pickMetricValue(args, [
      "ligand",
      "substrate_selection_pattern",
      "ligand_selection_pattern",
    ]);
    spiModel.region_pattern = pickMetricValue(args, [
      "region_pattern",
      "pocket_selection_pattern",
    ]);
    spiModel.Protein = pickMetricValue(args, ["Protein", "protein_selection_pattern"]);
  } else if (data.label === "RMSD") {
    model.openRMSD = true;
    RMSDModel.region_pattern = pickMetricValue(args, [
      "region_pattern",
      "pocket_selection_pattern",
    ]);
  } else if (data.label === "MMPBSA") {
    model.openMMPBSA = true;
    MMPBSAModel.ligand = pickMetricValue(args, [
      "ligand",
      "ligand_selection_pattern",
    ]);
  } else if (data.label === "Cavity Volume") {
    model.openCavity = true;
    cavityModel.ligand_selection_pattern = pickMetricValue(args, [
      "ligand_selection_pattern",
      "ligand",
    ]);
    cavityModel.pocket_compositing_residue_pattern = pickMetricValue(args, [
      "pocket_compositing_residue_pattern",
      "pocket_selection_pattern",
      "region_pattern",
    ]);
  } else if (data.label === "DSI") {
    model.openDSI = true;
    dsiModel.domain1_sequence = pickMetricValue(args, ["domain1_sequence"]);
    dsiModel.domain2_sequence = pickMetricValue(args, ["domain2_sequence"]);
  } else if (data.label === "DDG Fold") {
    message.info("DDG Fold does not require additional inputs.");
  }
};

const changeMetrics = item => {
  if (item.disabled) return;
  item.checked = !item.checked;
};

const addConstraint = () => {
  constraintsModel.value.push(buildConstraintRow());
};

const removeConstraint = index => {
  constraintsModel.value.splice(index, 1);
  if (!constraintsModel.value.length) {
    constraintsModel.value.push(buildConstraintRow());
  }
};

const handleConstraintTypeChange = constraint => {
  normalizeConstraintRow(constraint);
};

const saveConstraints = () => {
  const normalized = constraintsModel.value.map(item => normalizeConstraintRow(item));
  for (const constraint of normalized) {
    if (!constraint.type) {
      message.error("Please select a constraint type.");
      return;
    }
    if (constraint.arguments.some(arg => !arg)) {
      message.error("Please fill in all atoms for each constraint.");
      return;
    }
  }

  const payload = normalized.map(item => ({
    type: item.type,
    arguments: item.arguments,
  }));

  const formsData = new FormData();
  formsData.append("constraints", JSON.stringify(payload));
  constraintsSaving.value = true;
  updateExperimentProfile(route.query.id, formsData)
    .then(res => {
      if (res?.is_successful === false) {
        message.error(res.message || "Failed to update constraints.");
        return;
      }
      openConstraint.value = false;
    })
    .catch(() => {
      message.error("Failed to update constraints.");
    })
    .finally(() => {
      constraintsSaving.value = false;
    });
};

const saveEF = () => {
  let EF = metricsList.value.find(item => item.label === "EF");
  EF.data.arguments = Object.assign({}, efModel);
  model.openEF = false;
};

const saveSpi = () => {
  let SPI = metricsList.value.find(item => item.label === "SPI");
  SPI.data.arguments = Object.assign({}, spiModel);
  model.openSPI = false;
};

const saveRMSD = () => {
  let RMSD = metricsList.value.find(item => item.label === "RMSD");
  RMSD.data.arguments = Object.assign({}, RMSDModel);
  model.openRMSD = false;
};

const saveMMPBSA = () => {
  let MMPBSA = metricsList.value.find(item => item.label === "MMPBSA");
  MMPBSA.data.arguments = Object.assign({}, MMPBSAModel);
  model.openMMPBSA = false;
};

const saveCavity = () => {
  let cavity = metricsList.value.find(item => item.label === "Cavity Volume");
  cavity.data.arguments = Object.assign({}, cavityModel);
  model.openCavity = false;
};

const saveDSI = () => {
  let dsi = metricsList.value.find(item => item.label === "DSI");
  dsi.data.arguments = Object.assign({}, dsiModel);
  model.openDSI = false;
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

const saveMdLength = () => {
  const parsed = Number(mdLengthInput.value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    message.error("Please enter a valid MD simulation duration.");
    return;
  }

  const formsData = new FormData();
  formsData.append("md_length", parsed);
  mdLengthSaving.value = true;
  updateExperimentProfile(route.query.id, formsData)
    .then(res => {
      if (res?.is_successful === false) {
        message.error(res.message || "Failed to update MD simulation duration.");
        return;
      }
      mdLengthValue.value = parsed;
      openMdLength.value = false;
    })
    .catch(() => {
      message.error("Failed to update MD simulation duration.");
    })
    .finally(() => {
      mdLengthSaving.value = false;
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

.constraints-drawer {
  .constraint-list {
    margin-top: 8px;
  }

  .constraint-row {
    border: 1px solid #c6c6c6;
    border-radius: 3px;
    padding: 12px 12px 16px;
    margin-bottom: 12px;
  }

  .row-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .row-actions .icon {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }

  .row-body {
    margin-top: 12px;
  }

  .add-constraint {
    color: #0f62fe;
    cursor: pointer;
    font-size: 14px;
    margin: 8px 0 16px;
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
