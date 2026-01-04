<script setup>
import { ref, nextTick, watch, h, onMounted } from "vue";
import { getAssistants ,get_pdb_file} from "@/api/experiment";
import { useRoute } from "vue-router";
import { SendOutlined } from "@ant-design/icons-vue";
import Cube from "@/assets/img/cube.svg";
import user from "@/assets/img/self.svg";
import assistant from "@/assets/img/assistant.svg";
import toolCallResult from "./toolCallResult.vue";
import guiModal from "./guiModal.vue";
import { useUserStore } from "@/stores/user";

const route = useRoute(); // get current
const userStore = useUserStore();

const props = defineProps({
  defaultMessage: {
    type: Array,
    default: () => null,
  },
  preivew: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["send"]);

// 预设的对话选项
const defaultPrompts = [
  "Help me find mutations that make the active site cavity larger.",
  "I am studying a bidomain enzyme. This enzyme showed cold-adaption behavior, that is, the catalytic activity reduces much slower in lower temperatures. We found that just by changing the linker, the cold-adaption changes, can you help me perform some modeling to find linkers that provide stronger cold-adaption?",
  "I'm building a machine-learning model to predict protein melting temperatures (Tm) and would like to incorporate MD-derived properties as features—could you help with that?",
  "How do mutations influence the binding of substrate in Kemp elimiase?",
];

const messageType = new Map([
  ["assistant", "MutexaGPT"],
  ["user", "You"],
]);

// 聊天记录
const messages = ref([
  {
    role: "assistant",
    text_value: `Hi ${userStore.user?.username}, how can I help you today?`,
  },
]);

watch(
  () => props.defaultMessage,
  () => {
    if (props.defaultMessage.length) {
      messages.value = props.defaultMessage;
    } else {
      messages.value = [
        {
          role: "assistant",
          text_value: `Hi ${userStore.user?.username}, how can I help you today?`,
        },
      ];
    }
  }
);

// 输入框内容
const inputMessage = ref("");

// 是否显示加载状态
const loading = ref(false);
const isTyping = ref(false);
const currentResponse = ref("");
const disabled = ref(true);
const showGUI = ref(false);

const toolData = ref({});

// 发送消息
const sendMessage = async text_value => {
  if (!text_value.trim()) return;

  // 添加用户消息
  messages.value.push({
    role: "user",
    text_value: text_value,
  });

  // 清空输入框
  inputMessage.value = "";

  // 模拟API请求
  loading.value = true;

  isTyping.value = true;

  const data = await getAssistants(route.query.id, { prompt: text_value });
  if (data.is_successful) {
    emit("send", data.configuration_stages);

    const aiResponse = data.response_content;
    // 逐字显示 AI 响应
    // let index = 0;
    // const typingTimer = setInterval(() => {
    // if (index < aiResponse.length) {
    //   currentResponse.value = aiResponse.slice(0, index + 1)
    //   index++
    // } else {
    //   clearInterval(typingTimer)

    // console.log(htmlContent, aiResponse)
    // 添加助手回复

    messages.value.push({
      role: "assistant",
      text_value: aiResponse,
    });

    // toolData.value = data;
    if (data.require_pdb_file) {

      messages.value.push({
        data: data,
      });
      toolData.value = data;
    }
    // 
    if (data.confirm_button) {
      let index = messages.value.findIndex(item => item.data?.confirm_button);
      if (index > -1) {
        messages.value.splice(index, 1);
      }
      messages.value.push({
        data: data,
      });
      toolData.value = data;
    }
    console.log(messages.value);

    currentResponse.value = "";
    isTyping.value = false;
    // }
    // }, 50)
  } else {
    isTyping.value = false;
  }

  loading.value = false;
};

const inputTemplate = text_value => {
  inputMessage.value = text_value;
  disabled.value = !inputMessage.value.trim();
};

const handleChange = () => {
  disabled.value = !inputMessage.value.trim();
};

const confirmFn = ({content, node}) => {
  toolData.value.confirm_button = false;
  messages.value.push({
    role: "assistant",
    text_value: content,
  });
  emit("send", node);
};

// 自动滚动到底部
const chatContainer = ref(null);

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const formattedText = text => {
  return marked.parse(text);
};

// 监听消息变化,自动滚动
watch(
  () => messages.value.length,
  () => {
    nextTick(() => {
      scrollToBottom();
    });
  }
);

onMounted(() => { });
</script>

<template>
  <div class="chat-container">
    <!-- 聊天记录区域 -->
    <div class="messages-container" ref="chatContainer">
      <div class="tips" v-if="!props.defaultMessage.length">
        <div class="sub-title">Set up experiment with AI</div>
        <p class="description">
          Use natural language to describe your enzyme engineering ideas to the AI.
          The AI will clarify your intentions and performs necessary computational tasks.
        </p>
      </div>
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div v-if="msg.role">
          <a-flex align="center">
            <img :src="msg.role == 'user' ? user : assistant" alt="" srcset="" />
            <div class="user-name">{{ messageType.get(msg.role) }}</div>
          </a-flex>
          <div class="message-content" v-html="formattedText(msg.text_value)"></div>
        </div>
        <!--  -->
        <toolCallResult v-else :data="msg.data" :experiment_id="$route.query.id" @confirmFn="confirmFn" :key="index" />
        <!-- v-if="messages.length > 1 && !props.preivew" -->
      </div>
      <!-- AI 输入动画 -->
      <div v-if="isTyping" class="message typing-message">
        <a-flex align="center">
          <img :src="assistant" alt="" srcset="" />
          <div class="user-name">MutexaGPT</div>
        </a-flex>
        <a-flex class="message-content" align="center">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span>{{ currentResponse }}</span>
        </a-flex>
      </div>

      <!-- 预设问题区域 -->
      <div class="prompts-wrapper" v-if="messages.length == 1">
        <div v-for="prompt in defaultPrompts" :key="prompt" @click="inputTemplate(prompt)" class="prompt-button">
          {{ prompt }}
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <a-flex class="input-container" v-if="!props.preivew">
      <!--  -->
      <a-textarea v-model:value="inputMessage" :bordered="false" :autoSize="{ maxRows: 5, minRows: 3 }" type="tearea"
        placeholder="Type in anything" class="message-input" @keyup.enter="sendMessage(inputMessage)"
        @change="handleChange" />

      <a-flex align="center" justify="center">
        <span class="word-count">{{ inputMessage.length }}/200</span>
        <a-tooltip title="show 3D structure">
          <a-button type="text" :icon="h('img', { src: Cube, class: 'icon' })" class="show-button button"
            @click="showGUI = true" />
        </a-tooltip>
          <!-- :disabled="!toolData.require_pdb_file" -->
        <a-tooltip title="send">
          <a-button type="primary" @click="sendMessage(inputMessage)" :loading="loading" :disabled="disabled"
            :icon="h(SendOutlined)" class="send-button button" />
        </a-tooltip>
      </a-flex>
    </a-flex>
  </div>
  <guiModal v-model="showGUI" :experiment_id="$route.query.id" v-if="showGUI"></guiModal>
</template>

<style scoped lang="scss">
.chat-container {
  display: flex;
  flex-direction: column;
  // height: 98%;
  // max-width: 48rem;
  margin: 0 auto;
  height: 70vh;

  .messages-container {
    padding: 1rem;
    /*  */
    // margin: 40px 0 20px 0;
    // height: 52vh;
    flex: 1;
    overflow-y: auto;

    .tips {
      margin: 30px 0;

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
}

.message {
  max-width: 85%;
  margin-bottom: 30px;
  border-radius: 0.5rem;

  .user-name {
    font-size: 14px;
    font-weight: bold;
    color: #000;
    margin-left: 10px;
  }

  .message-content {
    font-size: 16px;
    color: #161616;
    line-height: 24px;
    margin-top: 10px;
    margin-left: 33px;
  }
}

.prompts-wrapper {
  margin: 1rem 0;
  // border-top: 1px solid #E5E7EB;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;

  .prompt-button {
    padding: 10px;
    font-size: 0.875rem;
    background-color: #e6e9ed;
    border: none;
    height: 160px;
    width: 24%;
    border-radius: 5px 10px 10px 5px;
    cursor: pointer;
    transition: background-color 0.2s;
    overflow: hidden;
    word-break: break-word;
  }
}

.input-container {
  padding: 0.5rem;
  border-radius: 8px;
  background: #fff;
  // height: 80px;
  border: 1px solid #e0e0e0;

  .message-input {
    flex: 1;
    background: #fff;
    border-radius: 8px;

    textarea {
      height: 100% !important;

      overflow: auto;
      /* 允许滚动 */
      scrollbar-width: none;
      /* Firefox 浏览器隐藏滚动条 */
      -ms-overflow-style: none;
      /* IE 浏览器隐藏滚动条 */
    }

    textarea::-webkit-scrollbar {
      display: none;
      /* Webkit 浏览器（Chrome、Safari 等）隐藏滚动条 */
    }
  }

  .word-count {
    font-size: 12px;
    color: #a8a8a8;
    margin-right: 15px;
    margin-left: 40px;
  }

  .button {
    color: white;
    border-radius: 0.5rem;
   // cursor: pointer;
    transition: background-color 0.2s;

    .icon {
      font-size: 16px;
      cursor: inherit;
    }

    .anticon-send {
      font-size: 13px;
      margin-left: 3px;
    }
  }

  .show-button {
    background-color: #393939;
  }

  .send-button {
    margin-left: 16px;
  }
}

.typing-indicator {
  display: flex;
  margin-right: 10px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin-right: 4px;
  background-color: #888;
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {

  0%,
  100% {
    opacity: 0.4;
  }

  50% {
    opacity: 1;
  }
}
</style>
