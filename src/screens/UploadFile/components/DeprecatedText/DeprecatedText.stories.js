import { DeprecatedText } from ".";

export default {
  title: "Components/DeprecatedText",
  component: DeprecatedText,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    inputText: "Input text",
    size: "large",
    className: {},
    textOverflowClassName: {},
    divClassName: {},
    hasIcon: true,
    backgroundClassName: {},
    visible: true,
    visible1: true,
  },
};
