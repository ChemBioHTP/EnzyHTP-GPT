/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { UiShellLeftPanel } from "../UiShellLeftPanel";
import "./style.css";

export const NavigationSideBar = ({
  className,
}) => {
  return (
    <div className={`navigation-side-nav version-4 ${className}`}>
      <div className="frame-4">
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          linkText="Grid"
          selected={false}
          stateProp="enabled"
          type="link"
        />
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          linkText="Git Merge"
          selected={false}
          stateProp="enabled"
          type="link"
        />
      </div>
      <div className="frame-9">
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          linkText="Help"
          selected={false}
          stateProp="enabled"
          type="link"
        />
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          linkText="Feedback"
          selected={false}
          stateProp="enabled"
          type="link"
        />
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          linkText="Settings"
          selected={false}
          stateProp="enabled"
          type="link"
        />
      </div>
    </div>
  );
};

NavigationSideBar.propTypes = {
  UIShellLeftPanelStateProp: PropTypes.string,
  UIShellLeftPanelSelected: PropTypes.bool,
  UIShellLeftPanelStateProp1: PropTypes.string,
  UIShellLeftPanelLinkText: PropTypes.string,
  UIShellLeftPanelSelected1: PropTypes.bool,
};