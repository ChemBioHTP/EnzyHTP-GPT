import { Tile } from ".";

export default {
  title: "Components/Tile",
  component: Tile,
  argTypes: {
    type: {
      options: [ "multi-select", "single-select", "base"],
      control: { type: "select" },
    },
    stateProp: {
      options: [
        "enabled",
        "selected",
        "disabled",
      ],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    descText : "Description",
    showDesc : true,
    showTitle : true,
    titleText : "Title",
    type:"single-select",
    stateProp:"enabled",
    className:{},
    titleClassName:{},
    descClassName:{},
  },
};
