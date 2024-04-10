import { Tag } from ".";

export default {
  title: "Components/Tag",
  component: Tag,
  argTypes: {
    size: {
      options: ["medium", "small"],
      control: { type: "select" },
    },
    color: {
      options: [
        "teal",
        "gray",
        "cool-gray",
        "outline",
        "warm-gray",
        "blue",
        "high-contrast",
        "green",
        "magenta",
        "red",
        "purple",
        "cyan",
      ],
      control: { type: "select" },
    },
    state: {
      options: ["enabled", "focus", "hover", "skeleton", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    filter: true,
    tagText: "Tag",
    size: "medium",
    color: "teal",
    state: "enabled",
    className: {},
    labelClassName: {},
  },
};
