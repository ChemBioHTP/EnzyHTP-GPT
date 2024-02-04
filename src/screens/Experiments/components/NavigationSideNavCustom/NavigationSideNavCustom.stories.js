import { NavigationSideNavCustom } from ".";

export default {
  title: "Components/NavigationSideNavCustom",
  component: NavigationSideNavCustom,
  argTypes: {
    version: {
      options: ["v3", "v1", "version-5", "version-4", "v2"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    version: "v3",
    className: {},
  },
};
