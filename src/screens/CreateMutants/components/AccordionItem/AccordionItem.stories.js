import { AccordionItem } from ".";

export default {
  title: "Components/AccordionItem",
  component: AccordionItem,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["enabled", "focus", "hover", "skeleton", "disabled"],
      control: { type: "select" },
    },
    alignment: {
      options: ["right", "left"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    slot: true,
    contentText:
      "The accordion component delivers large amounts of content in a small space through progressive disclosure. The user gets key details about the underlying content and can choose to expand that content within the constraints of the accordion.",
    titleText: "Title of accordion",
    size: "large",
    stateProp: "enabled",
    alignment: "right",
    flush: true,
    expanded: true,
    className: {},
    hasDiv: true,
  },
};
