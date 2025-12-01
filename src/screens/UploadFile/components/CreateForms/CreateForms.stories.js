import { CreateForms } from ".";

export default {
  title: "Components/CreateForms",
  component: CreateForms,
  argTypes: {
    state: {
      options: ["success", "error", "empty"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    state: "success",
    className: {},
    sizeLargeStateWrapperDeprecatedTextBackgroundClassName: {},
  },
};
