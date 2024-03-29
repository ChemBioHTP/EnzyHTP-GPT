import { ToggleItem } from ".";

export default {
  title: "Components/ToggleItem",
  component: ToggleItem,
  argTypes: {
    size: {
      options: ["small", "default"],
      control: { type: "select" },
    },
    state: {
      options: ["read-only", "enabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    size: "small",
    state: "read-only",
    className: {},
  },
};
