<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { ArrowRightOutlined } from "@ant-design/icons-vue";
import VerticalStepper from "@/components/VerticalStepper.vue";
import HeadInfo from "./components/headInfo.vue";
import { getExperimentDetail, getMutations, slurm } from "@/api/experiment";
import { useRoute, useRouter } from "vue-router";
import { useExperimentStore } from "@/stores/experiment";
import MutationGenerrated from "./components/mutationGenerrated.vue";
import WorkFlowConfig from "./components/workFlowConfig.vue";
import { CheckCircleFilled, LoadingOutlined } from "@ant-design/icons-vue";
const experimentStore = useExperimentStore();
const route = useRoute();
const router = useRouter();
const experiment = ref({});
const spinning = ref(false);
const loading = ref(false);
const model = reactive({
    mutations: [],
})

const seleceIndex = ref(0);
const openRun = ref(false);
const currentStep = ref(1);
const steps = reactive([
    {
        title: "Set-up",
        icon: "process",
    },
    {
        title: "Workflow",
        icon: "wait",
    },
]);


watch(
    () => route.query.id,
    () => {
        init();
    }
);

const getExperiment = async () => {
    spinning.value = true;
    getExperimentDetail(route.query.id).then(res => {
        spinning.value = false;
        experiment.value = res;
        experimentStore.setExperiment(res);
    }).finally(() => {
        spinning.value = false;
    });
};

const getMutationsList = () => {
    getMutations(route.query.id).then(res => {
        if (res.is_successful) {
            model.mutations = res.mutant_string_list;
        }
        console.log(res, "getMutations");
    })
}

const init = () => {
    getExperiment();
    getMutationsList();
}

const handleBack = () => {
    router.go(-1);
};

const handleSelect = (index) => {
    seleceIndex.value = index;
};

const handleStep = (index) => {
    console.log(index, "handleStep");
    if (index == 0) {
        router.push({ path: "/setup", query: { id: route.query.id, type: "Setup" } });
    }
}

const handleCreate = () => {
    if (seleceIndex.value == 0) {
        if (loading.value) return;
        loading.value = true;
        slurm(route.query.id).then(res => {
            loading.value = false;
            if (res.is_successful) {
                router.push({ path: "/result", query: { id: route.query.id, type: "Results" } })
            }
            console.log(res);
        })
    } else {
        // 
        openRun.value = false;
        router.push({ path: "/download", query: { id: route.query.id } })
    }
};


const runOption = ref([
    { title: "Let Our System Handle It", description: "Ideal if you don't have a service or prefer convenience. May take longer." },
    { title: "Run MD Simulation Yourself", description: "Ideal if you have your own tool or service to run the MD simulation." }
]);


onMounted(() => {
    // getMutationsGenerate(route.query.id).then(res => {
    //     console.log(res, "getMutations");
    // });
    init();
});
</script>

<template>
    <a-flex class="container">
        <div class="workflow-box">
            <a-spin :spinning="spinning" class="spinning"></a-spin>
            <div class="container" v-show="!spinning">
                <HeadInfo :experiment="experimentStore.experiment" />
                <a-flex class="box-content" justify="space-between">
                    <VerticalStepper :steps="steps" v-model="currentStep" @change="handleStep" class="steps mt30" />
                    <div class="workflow-content mt30">
                        <div class="tips">
                            <div class="sub-title">Review your simulation plan</div>
                            <p class="description">
                                This is the simulation plan configured by MutexaGPT. Please review it before running the experiment.
                                You can also change some configurations manually on this page.
                            </p>
                        </div>
                        <!--  -->
                        <WorkFlowConfig :metrics="experiment?.metrics" />
                    </div>
                    <div class="list">
                        <MutationGenerrated :mutations="model.mutations" />
                    </div>
                </a-flex>
                <a-flex class="footer" justify="end" align="center">
                    <a-button type="primary" ghost size="large" style="width: 74px;" @click="handleBack">
                        <a-flex class="button-content" justify="space-between" align="center">
                            <span>Back</span>
                        </a-flex>
                    </a-button>

                    <a-button type="primary" size="large" style="width: 180px;" class="ml10" @click="openRun = true">
                        <a-flex class="button-content" justify="space-between" align="center">
                            <span>Run experiment</span>
                            <ArrowRightOutlined />
                        </a-flex>
                    </a-button>
                </a-flex>
            </div>
        </div>
    </a-flex>
    <a-modal v-model:open="openRun" destroyOnClose @cancel="openRun = false" title="Choose Your MD Simulation Option"
        :footer="null" width="780px" wrapClassName="run-modal">
        <div>
            <p>Please select one of the options below based on your preference and resources:</p>
            <a-flex class="select-wrap" gap="middle">
                <div :class="['item', index == seleceIndex ? 'selected' : '']" @click="handleSelect(index)"
                    v-for="(item, index) in runOption">
                    <a-flex justify="space-between" align="center">
                        <div>{{ item.title }}</div>
                        <CheckCircleFilled style="#000" class="icon" />
                    </a-flex>
                    <div class="description"> {{ item.description }}</div>
                </div>

            </a-flex>
            <div class="mt24">
                <a-checkbox>Set as default. You won't be prompted again, but you can adjust this in the experiment
                    settings.</a-checkbox>
            </div>
            <div class="mt40"></div>
            <a-form-item>
                <a-flex class="btn-group">
                    <div @click="openRun = false" class="btn">Cancel</div>
                    <a-button type="primary" size="large" :disabled="disabled" @click="handleCreate" class="btn">
                        <a-flex class="button-content" justify="space-between" align="center">
                            <span>{{ seleceIndex == 0 ? 'Run experiment' : 'Next' }}</span>
                            <LoadingOutlined v-if="loading" class="ml20" />
                        </a-flex>
                    </a-button>
                </a-flex>
            </a-form-item>
        </div>
    </a-modal>
</template>
<style lang="scss" scoped>
.container {
    width: 100%;
    height: 100%;

    .workflow-box {
        flex: 1;
        width: 100%;
        height: 100%;

        .box-content {
            height: calc(100% - 210px);
            padding: 0 32px;
            overflow: hidden;

            .steps {
                width: 220px;
                height: 116px;
            }

            .workflow-content {
                width: 64%;

                .tips {
                    .sub-title {
                        color: #161616;
                        font-size: 20px;
                        font-weight: 600;
                    }

                    .description {
                        color: #525252;
                        font-size: 14px;
                        margin-top: 15px;
                        font-weight: 400;
                    }
                }


            }

            .list {
                width: 320px;
                // border-top: 1px solid #E0E0E0;
                border-left: 1px solid #E0E0E0;
                padding: 30px 17px;
                margin-left: 30px;
            }
        }

        .footer {
            border-top: 1px solid #e0e0e0;
            height: 100px;
            overflow: hidden;
            display: flex;
            align-items: center;

            .ant-btn.ant-btn-lg {
                height: 48px;
                margin-right: 35px;
            }
        }
    }

}



.run-modal {
    .select-wrap {
        .item {
            background-color: #fff;
            padding: 16px;
            font-size: 16px;
            color: #161616;
            width: 356px;
            cursor: pointer;
            box-sizing: border-box;
            margin-top: 30px;

            .description {
                font-size: 14px;
                color: #525252;
                margin-top: 15px;
            }

            .icon {
                display: none;
            }

            &.selected {
                border: 1px solid #000;

                .icon {
                    display: inline-block;
                }
            }
        }

    }
}
</style>
