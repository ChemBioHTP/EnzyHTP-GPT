import React, { useEffect, useState } from "react";
import { NavigationPage } from "../components/NavigationPage";
import { TabsItems } from "../components/TabsItems";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import "./style.css";
import { useNavigate } from "react-router-dom";
import {ProgressBarTrack} from "../components/ProgressBarTrack"
import  progressImage from "../../../assets/images/Experiments/ElementCreateResult/health-care-health-research.png"

export const ElementCreateResult = ({ sideVisible = true,  titleText= "My awesome experiment", onClickWrapper = () => { }}) => {
  const handleWrapperClick = (id) => {
    onClickWrapper(id);
  };

  useEffect(() => {
    if (sideVisible) {
      document.body.style.setProperty('--result-left-distance', '0px');
    } else {
      document.body.style.setProperty('--result-left-distance', '-214px');
    }

  }, [sideVisible]);

  let navigate = useNavigate();


  const handleBackToList = () => {
    let path = '/exp'; 
    navigate(path);
  };

  return (
    <div className="element-create-result">      
      <NavigationPage
        buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
        className="navigation-page-header"
        override={<IconAlertCircle2 className="icon-instance-node-3" />}
        onClick={handleBackToList}
        titleText={titleText}
      />
      <div className="frame-11">
        <TabsItems
          alignment="auto-width"
          className="tabs-items-instance"
          labelText="Input"
          selected={false}
          size="medium"
          stateProp="enabled"
          style="line"
          type="text-icon"
        />
        <TabsItems
          alignment="auto-width"
          className="tabs-items-instance"
          labelText="Results"
          selected
          size="medium"
          stateProp="selected"
          style="line"
          type="text-icon"
        />
      </div>
      <div className="frame-58">
        <img className="health-care-health" alt="Health care health" src={progressImage} />
        <div className="div-progress-text">
          <div className="label">MD simulation in progress</div>
          <p className="description">Your target metrics will be visible once the process is done.</p>
          <div className="div-progress">
            <ProgressBarTrack className="progress-bar-track-item" progress="twenty-five" size="big" />
            <div className="text-wrapper">25%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ElementCreateResult;
