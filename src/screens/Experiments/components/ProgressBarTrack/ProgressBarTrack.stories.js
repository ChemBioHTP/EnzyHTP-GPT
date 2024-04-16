import { ProgressBarTrack } from ".";

export default {
  title: "Components/ProgressBarTrack",
  component: ProgressBarTrack,
  argTypes: {
    progress: {
      options: ["indeterminate", "twenty-five", "zero", "success", "fifty", "seventy-five", "error"],
      control: { type: "select" },
    },
    size: {
      options: ["small", "big"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    progress: "indeterminate",
    size: "small",
    className: {},
  },
};
