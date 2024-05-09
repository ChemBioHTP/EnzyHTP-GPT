import { ProgressStatusBar } from ".";

export default {
  title: "Components/GenerateStatusBar",
  component: ProgressStatusBar,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["success", "loading", "uploaded", "error"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    longDesc: "Optional secondary explanation that can go on for two lines.",
    shortDesc: "File exceeds size limit.",
    text: "Filename.png",
    size: "large",
    stateProp: "success",
    className: {},
  },
};
