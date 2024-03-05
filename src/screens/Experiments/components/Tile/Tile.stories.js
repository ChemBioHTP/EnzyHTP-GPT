import { Tile } from ".";

export default {
  title: "Components/Tile",
  component: Tile,
  argTypes: {
    type: {
      options: ["expandable-interactive", "multi-select", "single-select", "base", "expandable", "clickable"],
      control: { type: "select" },
    },
    stateProp: {
      options: [
        "enabled-selected",
        "focus-selected",
        "hover-expanded",
        "enabled",
        "focus",
        "hover-selected",
        "hover",
        "focus-expanded",
        "enabled-expanded",
        "disabled",
      ],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    margin: false,
    descText: "Description",
    showDesc: true,
    slot: false,
    showTitle: true,
    titleText: "Title",
    accessible: true,
    type: "expandable-interactive",
    stateProp: "enabled-selected",
    className: {},
    divClassName: {},
    divClassNameOverride: {},
  },
};
