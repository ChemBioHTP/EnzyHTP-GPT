import { Button } from ".";

export default {
  title: "Components/Button",
  component: Button,
  argTypes: {
    style: {
      options: ["danger-ghost", "tertiary", "danger-primary", "secondary", "primary", "danger-tertiary", "ghost"],
      control: { type: "select" },
    },
    type: {
      options: ["icon-only", "text-icon"],
      control: { type: "select" },
    },
    size: {
      options: ["large", "two-x-large", "extra-large", "expressive", "small", "medium"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["active", "enabled", "focus", "hover", "skeleton", "disabled"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    icon: true,
    resizer: false,
    buttonText: "Button",
    style: "danger-ghost",
    type: "icon-only",
    size: "large",
    stateProp: "active",
    className: {},
    iconClassName: {},
    divClassName: {},
    divClassNameOverride: {},
  },
};
