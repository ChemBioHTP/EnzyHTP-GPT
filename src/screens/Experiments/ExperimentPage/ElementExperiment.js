import React from "react";
import { useState, useReducer, useEffect} from 'react';
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { BrowserRouter as Router, Route, Routes, Navigate, useNavigate } from 'react-router-dom';

import "./style.css";
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";
import ElementCreateWorkFlow from "../CreateWorkFLow/ElementCreateWorkFlow";
import ElementCreateTarget from "../CreateTarget/ElementCreateTarget";
import ElementExperimentsList from "../ExperimentsList/ElementExperimentsList";

export const ElementExperiment = () => {
  const [isVisible, setIsVisible] = useState(true);
  let navigate = useNavigate();
  const [sideLabel, setSideLabel] = useState(["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"]);
  const [titleText, setTitleText] = useState("Example experiment 01");
  const handleButtonClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
    if (buttonId > 5) {
      setTitleText(sideLabel[buttonId - 6]);
    }
  };

  const handleSideBarClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
  };

  const handleWrapperClick = (id) => {
    if (id === 0) {
      let path = '/exp/create'; 
      navigate(path);
    } else {
      let path = '/exp/flow'; 
      navigate(path);
    }
  };

  return (
    <div className="element-experiment" data-theme-mode="white-theme">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <Routes>
          <Route path="/" element={<ElementExperimentsList sideVisible={isVisible} />} />
          <Route path="/flow" element={<ElementCreateWorkFlow sideVisible={isVisible} onClickWrapper={handleWrapperClick}/>} />
          <Route path="/create" element={<ElementCreateTarget sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick} />} />
        </Routes>
        <NavigationHeader className="navigation-header-instance" />
        
        <NavigationSideBar className="navigation-side-nav-instance" onButtonClick={handleSideBarClick} />
        
        {isVisible && <NavigationSideNav
          UIShellLeftPanelLinkText={sideLabel}
          UIShellLeftPanelSelected1={[false, false, false, false, false]}
          UIShellLeftPanelStateProp1={["enabled", "enabled", "enabled", "enabled", "enabled"]}
          className="navigation-side-nav-2"
          version="version-5"
          onButtonClick={handleButtonClick}
        />}
        
      </div>
    </div>
  );
};

export default ElementExperiment;