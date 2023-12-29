import { FileUploaderDrag } from ".";

export default {
  title: "Components/FileUploaderDrag",
  component: FileUploaderDrag,
  argTypes: {
    state: {
      options: ["disabled", "drag-hover", "focus", "enabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    helperText: "Drag and drop files here or click to upload",
    state: "disabled",
    className: {},
  },
};
