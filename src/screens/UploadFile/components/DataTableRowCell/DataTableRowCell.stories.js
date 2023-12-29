import { DataTableRowCell } from ".";

export default {
  title: "Components/DataTableRowCell",
  component: DataTableRowCell,
  argTypes: {
    size: {
      options: ["large", "extra-large", "extra-small", "small", "medium"],
      control: { type: "select" },
    },
    state: {
      options: ["disabled", "focus", "enabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    showText: true,
    cellText: "Content",
    slot: false,
    size: "large",
    state: "disabled",
    className: {},
    minHeightClassName: {},
    resizerResizerClassName: {},
  },
};
