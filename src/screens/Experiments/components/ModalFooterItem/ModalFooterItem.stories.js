import { ModalFooterItem } from ".";

export default {
  title: "Components/ModalFooterItem",
  component: ModalFooterItem,
  argTypes: {
    actions: {
      options: ["two", "three", "one"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    actions: "two",
    cancel: true,
    className: {},
    buttonButtonText: "Button",
    buttonButtonText1: "Button",
  },
};
