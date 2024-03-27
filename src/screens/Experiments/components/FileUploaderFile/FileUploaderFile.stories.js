import { FileUploaderFile } from ".";

export default {
  title: "Components/FileUploaderFile",
  component: FileUploaderFile,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["success", "focus", "loading", "uploaded", "error-long", "error-short"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    longDesc: "Optional secondary explanation that can go on for two lines.",
    shortDesc: "File exceeds size limit.",
    fileName: "Filename.png",
    size: "large",
    stateProp: "success",
    className: {},
  },
};
