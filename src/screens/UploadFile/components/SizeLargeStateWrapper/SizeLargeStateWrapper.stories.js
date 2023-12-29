import { SizeLargeStateWrapper } from ".";

export default {
  title: "Components/SizeLargeStateWrapper",
  component: SizeLargeStateWrapper,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    state: {
      options: ["warning", "active", "enabled", "focus", "skeleton", "error", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    labelText: "Label",
    showLabel: true,
    errorText: "Error message goes here",
    showHelper: true,
    helperText: "Helper text",
    warningText: "Warning message goes here",
    size: "large",
    state: "warning",
    filled: true,
    className: {},
    DEPRECATEDTextBackgroundClassName: {},
    DEPRECATEDTextInputText: "Input text",
  },
};
