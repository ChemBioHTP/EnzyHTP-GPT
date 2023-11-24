import { DirectionHorizontalWrapper } from ".";

export default {
  title: "Components/DirectionHorizontalWrapper",
  component: DirectionHorizontalWrapper,
  argTypes: {
    direction: {
      options: ["vertical", "horizontal"],
      control: { type: "select" },
    },
    state: {
      options: ["completed", "incomplete", "current", "skeleton", "error", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    optionalLabel: true,
    labelText: "Optional label",
    direction: "vertical",
    state: "completed",
    className: {},
    progressIndicatorStepText: "Step",
  },
};
