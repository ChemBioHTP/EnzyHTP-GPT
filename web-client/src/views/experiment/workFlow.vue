<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { ArrowRightOutlined, InboxOutlined } from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
import VerticalStepper from "@/components/VerticalStepper.vue";
import HeadInfo from "./components/headInfo.vue";
import {
    getExperimentDetail,
    getMutations,
    slurm,
    deployAccre,
    getThirdPartySoftwareAuthorization,
    submitThirdPartySoftwareAuthorization,
} from "@/api/experiment";
import { useRoute, useRouter } from "vue-router";
import { useExperimentStore } from "@/stores/experiment";
import MutationGenerrated from "./components/mutationGenerrated.vue";
import WorkFlowConfig from "./components/workFlowConfig.vue";
import { CheckCircleFilled, LoadingOutlined } from "@ant-design/icons-vue";
import { downloadFile } from "@/utils/common";
const experimentStore = useExperimentStore();
const route = useRoute();
const router = useRouter();
const experiment = ref({});
const spinning = ref(false);
const loading = ref(false);
const downloading = ref(false);
const model = reactive({
    mutations: [],
})

const seleceIndex = ref(0);
const openRun = ref(false);
const openThirdPartyAuthorization = ref(false);
const currentStep = ref(1);
const SYSTEM_MANAGED_BACKEND_KEY = "system_slurm";
const authorizationForm = reactive({
    loading: false,
    submitting: false,
    confirmed: false,
    fileList: [],
    requiredSoftware: [],
    missingSoftware: [],
    authorizations: {},
    reviewNote: "",
});
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

const syncAuthorizationModalState = (res) => {
    authorizationForm.requiredSoftware = res.required_software || [];
    authorizationForm.missingSoftware = res.missing_software || authorizationForm.requiredSoftware;
    authorizationForm.authorizations = res.authorizations || {};
    authorizationForm.reviewNote = "";
    const rejectedAuthorization = authorizationForm.missingSoftware
        .map(software => authorizationForm.authorizations[software.key])
        .find(authorization => authorization?.status === "rejected");
    if (rejectedAuthorization?.review_note) {
        authorizationForm.reviewNote = rejectedAuthorization.review_note;
    }
};

const getBlockingAuthorizationStatus = () => {
    const missingSoftware = authorizationForm.missingSoftware || [];
    for (const software of missingSoftware) {
        const authorization = authorizationForm.authorizations[software.key];
        if (authorization?.status) {
            return authorization.status;
        }
    }
    return missingSoftware.length ? "missing" : "verified";
};

const openAuthorizationModal = (res = {}) => {
    syncAuthorizationModalState(res);
    authorizationForm.confirmed = false;
    authorizationForm.fileList = [];
    openRun.value = false;
    openThirdPartyAuthorization.value = true;
};

const submitSlurmJob = () => {
    if (loading.value) return;
    loading.value = true;
    slurm(route.query.id)
        .then(res => {
            if (res.requires_third_party_software_authorization) {
                syncAuthorizationModalState(res);
                const blockingStatus = getBlockingAuthorizationStatus();
                if (blockingStatus === "pending_review") {
                    openRun.value = false;
                    message.info("Your third-party software authorization is pending admin review.");
                    return;
                }
                openAuthorizationModal(res);
                return;
            }
            if (res.is_successful) {
                router.push({ path: "/result", query: { id: route.query.id, type: "Results" } })
            }
            console.log(res);
        })
        .finally(() => {
            loading.value = false;
        });
};

const handleSystemManagedRun = () => {
    if (loading.value || authorizationForm.loading) return;
    authorizationForm.loading = true;
    getThirdPartySoftwareAuthorization({ backend: SYSTEM_MANAGED_BACKEND_KEY })
        .then(res => {
            syncAuthorizationModalState(res);
            if ((res.missing_software || []).length > 0) {
                const blockingStatus = getBlockingAuthorizationStatus();
                if (blockingStatus === "pending_review") {
                    openRun.value = false;
                    message.info("Your third-party software authorization is pending admin review.");
                    return;
                }
                openAuthorizationModal(res);
                return;
            }
            submitSlurmJob();
        })
        .finally(() => {
            authorizationForm.loading = false;
        });
};

const handleCreate = () => {
    if (seleceIndex.value == 0) {
        handleSystemManagedRun();
    } else {
        // 
        openRun.value = false;
        router.push({ path: "/download", query: { id: route.query.id } })
    }
};

const beforeAuthorizationUpload = file => {
    authorizationForm.fileList = [file];
    return false;
};

const removeAuthorizationUpload = () => {
    authorizationForm.fileList = [];
};

const handleAuthorizationSubmit = () => {
    if (authorizationForm.submitting) return;
    if (!authorizationForm.confirmed) {
        message.error("Please confirm that you are authorized to use the selected third-party software.");
        return;
    }
    if (!authorizationForm.fileList.length) {
        message.error("Please upload authorization documentation.");
        return;
    }

    const selectedFile = authorizationForm.fileList[0];
    const documentation = selectedFile.originFileObj || selectedFile;
    const formData = new FormData();
    formData.append("backend", SYSTEM_MANAGED_BACKEND_KEY);
    formData.append("confirmed", "true");
    formData.append("documentation", documentation);

    authorizationForm.submitting = true;
    submitThirdPartySoftwareAuthorization(formData)
        .then(res => {
            if (res.is_successful) {
                message.success(res.message);
                openThirdPartyAuthorization.value = false;
                return;
            }
            syncAuthorizationModalState(res);
        })
        .finally(() => {
            authorizationForm.submitting = false;
        });
};

const handleExportAccrePack = () => {
    if (downloading.value) return;
    downloading.value = true;
    deployAccre(route.query.id)
        .then(res => {
            downloadFile(res, "accre-run-pack.zip");
        })
        .finally(() => {
            downloading.value = false;
        });
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
                        <WorkFlowConfig
                          :metrics="experiment?.metrics"
                          :constraints="experiment?.constraints"
                          :md-length="experiment?.md_length"
                        />
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

                    <a-button
                      size="large"
                      style="width: 240px;"
                      class="ml10"
                      :loading="downloading"
                      @click="handleExportAccrePack"
                    >
                        <a-flex class="button-content" justify="space-between" align="center">
                            <span>Export Reproducibility package</span>
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
                    :key="item.title"
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
                    <a-button type="primary" size="large" :disabled="loading || authorizationForm.loading" @click="handleCreate" class="btn">
                        <a-flex class="button-content" justify="space-between" align="center">
                            <span>{{ seleceIndex == 0 ? 'Run experiment' : 'Next' }}</span>
                            <LoadingOutlined v-if="loading || authorizationForm.loading" class="ml20" />
                        </a-flex>
                    </a-button>
                </a-flex>
            </a-form-item>
        </div>
    </a-modal>
    <a-modal
      v-model:open="openThirdPartyAuthorization"
      destroyOnClose
      title="Third-Party Software Authorization Required"
      :footer="null"
      width="720px"
      wrapClassName="third-party-authorization-modal"
      @cancel="openThirdPartyAuthorization = false"
    >
        <div class="authorization-content">
            <p>
                You selected a backend that may invoke third-party scientific software subject to independent license
                terms. To use this backend, you must confirm that you, your institution, or your organization holds all
                licenses, permissions, or authorizations required for the selected software and for this submitted job.
            </p>
            <p>
                Please upload documentation showing that your use is covered by the applicable license or authorization.
                Do not upload license keys, passwords, download credentials, or unredacted confidential agreements.
            </p>
            <a-alert
              v-if="authorizationForm.reviewNote"
              type="error"
              show-icon
              :message="`Previous submission rejected: ${authorizationForm.reviewNote}`"
              class="review-note"
            />

            <div class="software-section">
                <div class="section-title">Selected backend software:</div>
                <ul class="software-list">
                    <li v-for="software in authorizationForm.requiredSoftware" :key="software.key">
                        {{ software.label }}
                    </li>
                </ul>
            </div>

            <a-upload-dragger
              v-model:file-list="authorizationForm.fileList"
              name="documentation"
              :multiple="false"
              :max-count="1"
              :before-upload="beforeAuthorizationUpload"
              @remove="removeAuthorizationUpload"
              accept=".pdf,.png,.jpg,.jpeg,.txt,.doc,.docx"
            >
                <p class="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p class="ant-upload-text">Upload authorization documentation</p>
                <p class="ant-upload-hint">PDF, image, text, Word, or redacted documentation files are supported.</p>
            </a-upload-dragger>

            <a-checkbox v-model:checked="authorizationForm.confirmed" class="authorization-confirmation">
                I confirm that I am authorized to use the selected third-party software for this submitted job. I further
                confirm that this use is consistent with all applicable license terms, including restrictions on
                commercial use, redistribution, third-party services, remote access, and unauthorized users.
            </a-checkbox>

            <a-flex class="authorization-actions" justify="end" gap="middle">
                <a-button size="large" @click="openThirdPartyAuthorization = false">Cancel</a-button>
                <a-button
                  type="primary"
                  size="large"
                  :loading="authorizationForm.submitting"
                  @click="handleAuthorizationSubmit"
                >
                    Submit for Verification
                </a-button>
            </a-flex>
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

:deep(.third-party-authorization-modal) {
    .authorization-content {
        color: #161616;
        font-size: 14px;
        line-height: 1.55;

        p {
            margin-bottom: 14px;
        }

        .software-section {
            margin: 18px 0;

            .section-title {
                font-weight: 600;
                margin-bottom: 8px;
            }

            .software-list {
                margin: 0;
                padding-left: 20px;
            }
        }

        .review-note {
            margin: 16px 0;
        }

        .authorization-confirmation {
            display: flex;
            align-items: flex-start;
            margin-top: 20px;
            line-height: 1.5;
        }

        .authorization-actions {
            margin-top: 28px;
        }
    }
}
</style>
