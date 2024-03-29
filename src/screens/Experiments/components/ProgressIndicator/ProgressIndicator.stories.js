import { ProgressIndicator } from ".";

export default {
  title: "Components/ProgressIndicator",
  component: ProgressIndicator,
  argTypes: {
    stateProp: {
      options: ["active", "enabled", "focus", "tooltip", "hover", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    stepText: "Step",
    stateProp: "active",
    tooltip: true,
    className: {},
  },
};
