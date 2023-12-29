import { SearchDefault } from ".";

export default {
  title: "Components/SearchDefault",
  component: SearchDefault,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["enabled", "filled", "focus", "hover", "skeleton", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    placeholderText: "Search input text",
    queryText: "Typing",
    size: "large",
    stateProp: "enabled",
    expandable: true,
    expanded: true,
    className: {},
  },
};
