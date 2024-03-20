import React from "react";
import { Accordion } from "../components/Accordion"
import { useState, useReducer, useEffect} from 'react';
import { Button } from "../components/Button";
import { DirectionHorizontalWrapper } from "../components/DirectionHorizontalWrapper";
import { ModalPanel } from "../components/ModalPanel";
import { ModalPanelTargets } from "../components/ModalPanelTargets";
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationPage } from "../components/NavigationPage";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { TabsItems } from "../components/TabsItems";
import { CircleDash1 } from "../icons/CircleDash1";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconArrowRight } from "../icons/IconArrowRight";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import { IconSend } from "../icons/IconSend";
import { Incomplete } from "../icons/Incomplete";
import "./style.css";
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";

export const ElementExperiment = () => {
  const [isVisible, setIsVisible] = useState(true);

  const [titleText, setTitleText] = useState("Example experiment 01");

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
    <div className="element-create-target" data-theme-mode="white-theme">
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