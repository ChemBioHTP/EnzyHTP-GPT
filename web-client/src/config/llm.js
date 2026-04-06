export const LLM_PROVIDER_OPTIONS = [
  { label: "OpenAI", value: "openai" },
  { label: "Fireworks", value: "fireworks" },
];

export const LLM_MODEL_OPTIONS = {
  openai: [
    { label: "gpt-4o", value: "gpt-4o-2024-11-20" },
    { label: "gpt-4.1-mini", value: "gpt-4.1-mini" },
    { label: "gpt-5.4", value: "gpt-5.4-2026-03-05" },
  ],
  fireworks: [
    { label: "Qwen3.6 Plus", value: "accounts/fireworks/models/qwen3p6-plus" },
    { label: "MiniMax-M2.5", value: "accounts/fireworks/models/minimax-m2p5" },
    { label: "GLM-5", value: "accounts/fireworks/models/glm-5" },
    { label: "Kimi K2.5", value: "accounts/fireworks/models/kimi-k2p5" },
    { label: "GLM-4.7", value: "accounts/fireworks/models/glm-4p7" },
    { label: "Deepseek v3.2", value: "accounts/fireworks/models/deepseek-v3p2" },
    { label: "Gemma 4 26B A4B IT", value: "accounts/fireworks/models/gemma-4-26b-a4b-it" },
    { label: "Gemma 4 31B IT", value: "accounts/fireworks/models/gemma-4-31b-it" },
  ],
};

export const getDefaultModelByProvider = provider => {
  const modelOptions = LLM_MODEL_OPTIONS[provider] || [];
  return modelOptions.length > 0 ? modelOptions[0].value : "";
};

export const requiresApiKey = (provider, useCustomApiKey) => {
  return provider === "openai" || !!useCustomApiKey;
};
