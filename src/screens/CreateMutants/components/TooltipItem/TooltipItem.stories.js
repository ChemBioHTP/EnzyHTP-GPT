import { TooltipItem } from ".";

export default {
  title: "Components/TooltipItem",
  component: TooltipItem,
  argTypes: {
    type: {
      options: ["definition", "icon", "standard"],
      control: { type: "select" },
    },
    position: {
      options: ["left", "right", "top", "bottom"],
      control: { type: "select" },
    },
    alignment: {
      options: ["end", "center", "start"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    tooltipText: "Tooltip text",
    type: "definition",
    position: "left",
    alignment: "end",
    className: {},
  },
};
