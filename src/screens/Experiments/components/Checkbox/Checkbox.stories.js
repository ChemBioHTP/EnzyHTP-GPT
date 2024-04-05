import { Checkbox } from ".";

export default {
  title: "Components/Checkbox",
  component: Checkbox,
  argTypes: {
    stateProp: {
      options: ["warning", "skeleton", "enabled", "focus", "read-only", "invalid", "disabled"],
      control: { type: "select" },
    },
    selection: {
      options: ["checked", "indeterminate", "unchecked"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    warningText: "Warning message goes here",
    helperMessage: false,
    label: true,
    labelText: "Label",
    warningMessage: true,
    errorMessage: true,
    helperText: "Helper text goes here",
    errorText: "Error message goes here",
    valueText: "Checkbox label",
    value: true,
    indented: false,
    stateProp: "warning",
    selection: "checked",
    className: {},
  },
};
