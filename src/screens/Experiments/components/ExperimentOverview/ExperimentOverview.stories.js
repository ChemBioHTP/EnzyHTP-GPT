import { ExperimentOverview } from ".";

export default {
  title: "Components/ExperimentOverview",
  component: ExperimentOverview,
  argTypes: {
    type: {
      options: ["tags", "flow", "text"],
      control: { type: "select" },
    },
    stateProp: {
      options: ["hover", "default"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    heading: true,
    type: "tags",
    stateProp: "hover",
    heading1: true,
    className: {},
    text: "Target metrics",
    frameClassName: {},
    text1: "Please provide the prompt and run the experiment.",
    divClassName: {},
  },
};
