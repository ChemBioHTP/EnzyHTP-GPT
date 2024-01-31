import { StatusIcon } from ".";

export default {
  title: "Components/StatusIcon",
  component: StatusIcon,
  argTypes: {
    state: {
      options: ["success-blue", "info", "success-green", "warning-yellow", "warning-red", "error"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    state: "success-blue",
    highContrast: true,
    className: {},
  },
};
