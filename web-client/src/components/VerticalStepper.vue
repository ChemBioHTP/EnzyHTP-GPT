<!-- VerticalStepper.vue -->
<template>
    <div class="stepper-container">
        <!-- 左侧进度条 -->
        <div class="progress-bar-container">
            <div class="progress-block" v-for="(_, index) in steps" :key="index"
                :class="{ 'active': currentStep == index }"></div>
        </div>

        <!-- 右侧步骤内容 -->
        <div class="steps-container">
           
            <div v-for="(step, index) in steps" :key="index" :class="['step-item',step.disabled? 'disabled' : '']" @click="goToStep(index)" ref="stepRefs">
                <!-- 步骤图标 -->
                <div class="step-icon">
                    <img :src="currentStep > index ? finish : currentStep === index ? process : wait" />
                </div>

                <!-- 步骤内容 -->
                <div class="step-content">
                    <h3 class="step-title">{{ step.title }}</h3>
                    <p class="step-description">{{ step.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue';
import finish from "@/assets/img/finish.png";
import process from "@/assets/img/process.png";
import wait from "@/assets/img/wait.png";

const props = defineProps({
    steps: {
        type: Array,
        required: true,
    }
});

const currentStep = defineModel({ default: 0 })

const emit = defineEmits(['change']);

const stepRefs = ref([]);

// 跳转到指定步骤
const goToStep = (index) => {
    if (props.steps[index].disabled) {
        return;
    }
    currentStep.value = index;
    emit('change', index);
};

onMounted(() => {
    // 初始化
});
</script>

<style scoped>
.stepper-container {
    display: flex;
    gap: 0px;
}

.progress-bar-container {
    display: flex;
    flex-direction: column;
    position: relative;
}

.progress-block {
    flex: 1;
    width: 2px;
    background-color: #c6c6c6;
    transition: background-color 0.3s ease;
}

.progress-block.active {
    background-color: #0F62FE;
}

.steps-container {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.step-item {
    flex: 1;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding: 0 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.step-item:last-child {
    margin-bottom: 0;
}

.step-icon {
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;

    img {
        width: 100%;
        height: 100%;
    }
}

.step-content {
    flex: 1;
}

.step-title {
    margin: 0;
    font-size: 14px;
    color: #161616;
}

.step-description {
    margin: 8px 0 0;
    color: #666;
    font-size: 0.9em;
    line-height: 1.5;
}

/* 激活状态样式 */
.step-item.active .step-icon {
    /* background-color: #1976d2; */
    /* color: white; */
}

/* 当前步骤样式 */
.step-item.current {
    /* background-color: #e3f2fd; */
    /* border-color: #1976d2; */
    /* box-shadow: 0 2px 8px rgba(25, 118, 210, 0.1); */
}

/* 完成步骤的图标样式 */
.icon-check {
    font-size: 18px;
}
</style>