import { AccordionWith } from ".";

export default {
  title: "Components/AccordionWith",
  component: AccordionWith,
  argTypes: {
    state: {
      options: ["off", "on"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    state: "off",
    className: {},
  },
};
