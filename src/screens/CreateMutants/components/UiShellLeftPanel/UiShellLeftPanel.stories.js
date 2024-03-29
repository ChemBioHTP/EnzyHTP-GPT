import { UiShellLeftPanel } from ".";

export default {
  title: "Components/UiShellLeftPanel",
  component: UiShellLeftPanel,
  argTypes: {
    type: {
      options: ["link", "sub-menu", "divider", "compact"],
      control: { type: "select" },
    },
    level: {
      options: ["level-2", "level-1"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["active", "enabled", "selected", "focus", "softly-selected", "hover", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    linkText: "Link",
    iconRight: false,
    iconLeft: false,
    type: "link",
    level: "level-2",
    stateProp: "active",
    selected: true,
    expanded: true,
    compact: true,
    divider: true,
    className: {},
    linkIconClassName: {},
  },
};
