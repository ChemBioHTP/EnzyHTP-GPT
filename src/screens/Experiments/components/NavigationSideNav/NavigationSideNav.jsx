/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React, { useState } from "react";
import { UiShellLeftPanel } from "../../../../components/UiShellLeftPanel";
import HideNav from "../../../../assets/images/Experiments/hide-nav.svg"
import "./style.css";

export const NavigationSideNav = ({
  className,
  UIShellLeftPanelStateProp = ["enabled", "enabled", "enabled", "enabled", "enabled"],
  UIShellLeftPanelSelected = [false, false, false, false, false],
  UIShellLeftPanelStateProp1 = ["enabled", "enabled", "enabled", "enabled", "enabled"],
  UIShellLeftPanelLinkText = ["01", "02", "03", "04", "05"],
  UIShellLeftPanelSelected1 = [false, false, false, false, false],
  // call back function for button id which indicates selected tab (from 1-10)
  onButtonClick = () => {},
}) => {
  const [StateProp, setStateProp] = useState(UIShellLeftPanelStateProp);
  const [Selected, setSelected] = useState(UIShellLeftPanelSelected);
  const [StateProp1, setStateProp1] = useState(UIShellLeftPanelStateProp1);
  const [Selected1, setSelected1] = useState(UIShellLeftPanelSelected1);

  const handleButtonClick = (buttonId) => {
    onButtonClick(buttonId);
    const listItems = ["enabled", "enabled", "enabled", "enabled", "enabled"];
    const listItems1 = [false, false, false, false, false];
    const newListItems = ["enabled", "enabled", "enabled", "enabled", "enabled"];
    const newListItems1 = [false, false, false, false, false];

    if (buttonId < 6) {      
      setStateProp1(listItems);
      newListItems[buttonId - 1] = "selected";
      setStateProp(newListItems);  
      setSelected1(listItems1);
      newListItems1[buttonId - 1] = true;
      setSelected(newListItems1);
    } else {
      setStateProp(listItems);   
      newListItems[buttonId - 6] = "selected";
      setStateProp1(newListItems);  
      setSelected(listItems1);
      newListItems1[buttonId - 6] = true;
      setSelected1(newListItems1);
    }
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
            selected={Selected[0]}
            stateProp={StateProp[0]}
            onButtonClick={() => handleButtonClick(1)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="In progress"
            selected={Selected[1]}
            stateProp={StateProp[1]}
            onButtonClick={() => handleButtonClick(2)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="With error"
            selected={Selected[2]}
            stateProp={StateProp[2]}
            onButtonClick={() => handleButtonClick(3)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Complete"
            selected={Selected[3]}
            stateProp={StateProp[3]}
            onButtonClick={() => handleButtonClick(4)}
            type="link"
          />
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-2"
            linkText="Archived"
            selected={Selected[4]}
            stateProp={StateProp[4]}
            onButtonClick={() => handleButtonClick(5)}
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
          {UIShellLeftPanelLinkText.map((panelLinkText, index) => (
            <UiShellLeftPanel
              key={index}
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText={panelLinkText}
              selected={Selected1[index]}
              stateProp={StateProp1[index]}
              onButtonClick={() => handleButtonClick(6+index)}
              type="link"
            />
          ))}
          
        </div>
      </div>
    </div>
  );
};

NavigationSideNav.propTypes = {
  UIShellLeftPanelStateProp: PropTypes.array,
  UIShellLeftPanelSelected: PropTypes.array,
  UIShellLeftPanelStateProp1: PropTypes.array,
  UIShellLeftPanelLinkText: PropTypes.array,
  UIShellLeftPanelSelected1: PropTypes.array,
};
