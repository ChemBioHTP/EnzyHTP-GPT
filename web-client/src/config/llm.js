export const LLM_PROVIDER_OPTIONS = [
  { label: "OpenAI", value: "openai" },
  { label: "Fireworks", value: "fireworks" },
];

export const LLM_MODEL_OPTIONS = {
  openai: [
    { label: "gpt-4o-2024-11-20", value: "gpt-4o-2024-11-20" },
    { label: "gpt-4.1-mini", value: "gpt-4.1-mini" },
  ],
  fireworks: [
    { label: "Kimi K2.5", value: "accounts/fireworks/models/kimi-k2p5" },
    { label: "DeepSeek V3.1", value: "accounts/fireworks/models/deepseek-v3p1" },
  ],
};

export const getDefaultModelByProvider = provider => {
  const modelOptions = LLM_MODEL_OPTIONS[provider] || [];
  return modelOptions.length > 0 ? modelOptions[0].value : "";
};

export const requiresApiKey = (provider, useCustomApiKey) => {
  return provider === "openai" || !!useCustomApiKey;
};
