import { Slot } from ".";

export default {
  title: "Components/Slot",
  component: Slot,
  argTypes: {
    size: {
      options: ["small", "default"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    iconOnly: true,
    size: "small",
    className: {},
  },
};
