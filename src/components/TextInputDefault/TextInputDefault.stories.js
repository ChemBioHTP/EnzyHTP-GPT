import { TextInputDefault } from ".";

export default {
  title: "Components/TextInputDefault",
  component: TextInputDefault,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    state: {
      options: ["warning", "active", "enabled", "focus", "read-only", "skeleton", "error", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    countText: "0/100",
    labelText: "Label",
    showLabel: true,
    showCount: false,
    inputText: "Input text",
    placeholderText: "Placeholder text (optional)",
    errorText: "Error message goes here",
    showHelper: true,
    helperText: "Optional helper text",
    warningText: "Warning message goes here",
    size: "large",
    state: "warning",
    textFilled: true,
    className: {},
    spacerClassName: {},
    backgroundClassName: {},
    inputType: "text",
  },
};
