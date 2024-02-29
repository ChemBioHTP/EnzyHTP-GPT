/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React, { useState } from "react";
import { UiShellLeftPanel } from "../UiShellLeftPanel";
import HideNav from "../../../../assets/images/Experiments/hide-nav.svg"
import "./style.css";

export const NavigationSideNav = ({
  className,
  UIShellLeftPanelStateProp = "enabled",
  UIShellLeftPanelSelected = true,
  UIShellLeftPanelStateProp1 = ["selected", "enabled", "enabled", "enabled", "enabled"],
  UIShellLeftPanelLinkText = ["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"],
  UIShellLeftPanelSelected1 = [false,false, false, false, false],
  onButtonClick = () => {},
}) => {
  const [isStyled, setIsStyled] = useState(false);

  const handleButtonClick = (buttonId) => {
    onButtonClick(buttonId);
    setIsStyled(!isStyled);
  };

  return (
    <div className={`navigation-side-nav version-5 ${className}`}>
      <div className="frame-4">
        <div className="frame-5">     
          <div className="frame-5-1">   
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-1"
              linkText="My experiments"
              linkIconClassName="UI-shell-left-panel-instance"
              hideImg = {true}
              selected={false}
              stateProp="disabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-1"
              linkImg={HideNav}
              linkIconClassName="UI-shell-left-panel-instance"
              hideImg={false}
              hideText={true}
              selected={false}
              stateProp="enabled"
              type="link"
              onButtonClick={() => handleButtonClick(0)}
              />
          </div>
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
            linkText={UIShellLeftPanelLinkText[0]}
            selected={UIShellLeftPanelSelected1[0]}
            stateProp={UIShellLeftPanelStateProp1[0]}
            onButtonClick={() => handleButtonClick(1)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText={UIShellLeftPanelLinkText[1]}
            selected={UIShellLeftPanelSelected1[1]}
            stateProp={UIShellLeftPanelStateProp1[1]}
            onButtonClick={() => handleButtonClick(2)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText={UIShellLeftPanelLinkText[2]}
            selected={UIShellLeftPanelSelected1[2]}
            stateProp={UIShellLeftPanelStateProp1[2]}
            onButtonClick={() => handleButtonClick(3)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText={UIShellLeftPanelLinkText[3]}
            selected={UIShellLeftPanelSelected1[3]}
            stateProp={UIShellLeftPanelStateProp1[3]}
            onButtonClick={() => handleButtonClick(4)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText={UIShellLeftPanelLinkText[4]}
            selected={UIShellLeftPanelSelected1[4]}
            stateProp={UIShellLeftPanelStateProp1[4]}
            onButtonClick={() => handleButtonClick(5)}
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
  UIShellLeftPanelStateProp1: PropTypes.array,
  UIShellLeftPanelLinkText: PropTypes.array,
  UIShellLeftPanelSelected1: PropTypes.array,
};
