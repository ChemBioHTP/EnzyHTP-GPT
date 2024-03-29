import { TagCloseButton } from ".";

export default {
  title: "Components/TagCloseButton",
  component: TagCloseButton,
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
    stateProp: {
      options: ["disabled", "hover", "focus", "enabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    size: "medium",
    color: "teal",
    stateProp: "disabled",
    className: {},
    close97Color: "#150080",
  },
};
