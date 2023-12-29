import { DataTableToolbar } from ".";

export default {
  title: "Components/DataTableToolbar",
  component: DataTableToolbar,
  argTypes: {
    size: {
      options: ["XL-LG-MD", "SM-XS"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    size: "XL-LG-MD",
    className: {},
    visible: true,
    buttonIconClassName: {},
    buttonButtonText: "Button",
  },
};
