/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { UiShellLeftPanel } from "../UiShellLeftPanel";
import HideNav from "../../../../assets/images/Experiments/hide-nav.svg"
import "./style.css";

export const NavigationSideNav = ({
  className,
  UIShellLeftPanelStateProp = "selected",
  UIShellLeftPanelSelected = true,
  UIShellLeftPanelStateProp1 = "enabled",
  UIShellLeftPanelLinkText = "Example experiment 01",
  UIShellLeftPanelSelected1 = false,
}) => {
  return (
    <div className={`navigation-side-nav version-5 ${className}`}>
      <div className="frame-4">
        <div className="frame-5">          
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-1"
            linkText="My experiments"
            linkImg={HideNav}
            linkIconClassName="UI-shell-left-panel-instance"
            hideImg = {false}
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="All"
            selected={UIShellLeftPanelSelected}
            stateProp={UIShellLeftPanelStateProp}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="In progress"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="With error"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Complete"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Archived"
            selected={false}
            stateProp="enabled"
            type="link"
          />
        </div>       
      </div>
      <div className="frame-9">
        <div className="frame-10">
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider
            expanded={false}
            level="level-1"
            selected={false}
            stateProp="enabled"
            type="divider"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText={UIShellLeftPanelLinkText}
            selected={UIShellLeftPanelSelected1}
            stateProp={UIShellLeftPanelStateProp1}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Example experiment 02"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Example experiment 03"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Example experiment 04"
            selected={false}
            stateProp="enabled"
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Example experiment 05"
            selected={false}
            stateProp="enabled"
            type="link"
          />
        </div>
      </div>
    </div>
  );
};

NavigationSideNav.propTypes = {
  UIShellLeftPanelStateProp: PropTypes.string,
  UIShellLeftPanelSelected: PropTypes.bool,
  UIShellLeftPanelStateProp1: PropTypes.string,
  UIShellLeftPanelLinkText: PropTypes.string,
  UIShellLeftPanelSelected1: PropTypes.bool,
};
