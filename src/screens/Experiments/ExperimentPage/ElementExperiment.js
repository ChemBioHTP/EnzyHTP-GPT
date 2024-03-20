import React from "react";
import { useState, useReducer, useEffect} from 'react';
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationSideNav } from "../components/NavigationSideNav";

import "./style.css";
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";

export const ElementExperiment = () => {
  const [isVisible, setIsVisible] = useState(true);

  const [sideLabel, setSideLabel] = useState(["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"]);
  const handleButtonClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
  };

  const handleSideBarClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
  };

  return (
    <div className="element-experiment" data-theme-mode="white-theme">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        
        <NavigationSideBar className="navigation-side-nav-instance" onButtonClick={handleSideBarClick} />
        
        {isVisible && <NavigationSideNav
          UIShellLeftPanelLinkText={sideLabel}
          UIShellLeftPanelSelected1={[true, false, false, false, false]}
          UIShellLeftPanelStateProp1={["selected", "enabled", "enabled", "enabled", "enabled"]}
          className="navigation-side-nav-2"
          version="version-5"
          onButtonClick={handleButtonClick}
        />}
      </div>
    </div>
  );
};

export default ElementExperiment;