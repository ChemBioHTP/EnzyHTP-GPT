/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { UiShellLeftPanel } from "../UiShellLeftPanel";
import Grid from "../../assets/images/Experiments/grid.svg"
import GitMerge from "../../assets/images/Experiments/git-merge.svg"
import Help from "../../assets/images/Experiments/help.svg"
import Feedback from "../../assets/images/Experiments/feedback.svg"
import Settings from "../../assets/images/Experiments/settings.svg"
import "./style.css";

export const NavigationToolbar = ({
  className,
  onButtonClick = () => {},
}) => {
  const handleButtonClick = (buttonId) => {
    onButtonClick(buttonId);
  };
  return (
    <div className={`navigation-toolbar version-4 ${className}`}>
      <div className="frame-4">
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          hideImg={false}
          hideText={true}
          linkImg={Grid}
          selected={false}
          stateProp="enabled"
          type="link"
          onButtonClick={() => handleButtonClick(0)}
        />
        <UiShellLeftPanel
          className="UI-shell-left-panel-menu-item"
          compact={false}
          divider={false}
          expanded={false}
          level="level-1"
          linkIconClassName="UI-shell-left-panel-instance"
          hideImg={false}
          hideText={true}
          linkImg={GitMerge}
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
          hideImg={false}
          hideText={true}
          linkImg={Help}
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
          hideImg={false}
          hideText={true}
          linkImg={Feedback}
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
          hideImg={false}
          hideText={true}
          linkImg={Settings}
          selected={false}
          stateProp="enabled"
          type="link"
        />
      </div>
    </div>
  );
};

NavigationToolbar.propTypes = {
  UIShellLeftPanelStateProp: PropTypes.string,
  UIShellLeftPanelSelected: PropTypes.bool,
  UIShellLeftPanelStateProp1: PropTypes.string,
  UIShellLeftPanelLinkText: PropTypes.string,
  UIShellLeftPanelSelected1: PropTypes.bool,
};