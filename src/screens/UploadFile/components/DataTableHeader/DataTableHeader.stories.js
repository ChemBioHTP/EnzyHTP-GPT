import { DataTableHeader } from ".";

export default {
  title: "Components/DataTableHeader",
  component: DataTableHeader,
  argTypes: {
    size: {
      options: ["large", "extra-large", "extra-small", "small", "medium"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["hover", "selected", "enabled"],
      control: { type: "select" },
    },
    sorted: {
      options: ["ascending", "none", "descending"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    cellText: "Header",
    size: "large",
    stateProp: "hover",
    sorted: "ascending",
    sortable: true,
    className: {},
    resizerResizerClassName: {},
  },
};
