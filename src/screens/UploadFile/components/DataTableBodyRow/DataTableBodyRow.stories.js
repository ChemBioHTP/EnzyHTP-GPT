import { DataTableBodyRow } from ".";

export default {
  title: "Components/DataTableBodyRow",
  component: DataTableBodyRow,
  argTypes: {
    size: {
      options: ["large", "extra-large", "extra-small", "small", "medium"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    slot: false,
    text: true,
    cellText: "Expandable table content",
    size: "large",
    className: {},
    minHeightClassName: {},
    descriptionClassName: {},
    contentClassName: {},
    border: "/img/border.svg",
  },
};
