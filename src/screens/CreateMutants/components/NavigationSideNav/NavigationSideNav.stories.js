import { NavigationSideNav } from ".";

export default {
  title: "Components/NavigationSideNav",
  component: NavigationSideNav,
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
    UIShellLeftPanelStateProp: "selected",
    UIShellLeftPanelSelected: true,
    UIShellLeftPanelStateProp1: "enabled",
    UIShellLeftPanelLinkText: "Example experiment 01",
    UIShellLeftPanelSelected1: false,
  },
};
