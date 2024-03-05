import { TabsItems } from ".";

export default {
  title: "Components/TabsItems",
  component: TabsItems,
  argTypes: {
    style: {
      options: ["line", "contained"],
      control: { type: "select" },
    },
    type: {
      options: ["icon-only", "text-icon"],
      control: { type: "select" },
    },
    size: {
      options: ["large", "medium"],
      control: { type: "select" },
    },
    alignment: {
      options: ["auto-width", "grid-aware"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["enabled", "selected", "focus", "hover", "skeleton", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    hoverDimissible: false,
    show2NdLabel: false,
    divider: true,
    dismissibleIcon: false,
    labelText: "Tab label",
    dismissible: false,
    icon: false,
    style: "line",
    type: "icon-only",
    size: "large",
    alignment: "auto-width",
    stateProp: "enabled",
    selected: true,
    className: {},
  },
};
