import React, { useEffect, useState } from "react";
import { NavigationPage } from "../components/NavigationPage";
import { TabsItems } from "../components/TabsItems";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import "./style.css";
import { useNavigate } from "react-router-dom";
import {ProgressBarTrack} from "../components/ProgressBarTrack"
import  progressImage from "../../../assets/images/Experiments/ElementCreateResult/health-care-health-research.png"
import { DataTableRowCell } from "../components/DataTableRowCell";
import HideNav from "../../../assets/images/Experiments/hide-nav.svg"
import { DataTable } from "../../../components/DataTable";

export const ElementCreateResult = ({ sideVisible = true,  titleText= "exp-test-03", progerss="zero"}) => {

  useEffect(() => {
    if (sideVisible) {
      document.body.style.setProperty("--result-left-distance", "0px");
    } else {
      document.body.style.setProperty("--result-left-distance", "-214px");
    }
  }, [sideVisible]);

  let navigate = useNavigate();

  const cellData = [
    ["WT structure (fixed)",".pdb" ], 
    // ["MD instruction file",".in"], 
    // ["MD constraint file",".rs"],
  ];

  const handleBackToList = () => {
    let path = "/exp";
    navigate(path);
  };

  const handleProgressNum = (progress) => {
    if(progerss=="zero"){
        return "0%";
    } else if(progerss=="twenty-five"){
        return "25%";
    } else if(progerss=="fifty"){
        return "50%";
    } else if(progerss=="seventy-five"){
        return "75%";
    } else if(progerss=="success"){
        return "100%";
    }


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
        <img
          className="health-care-health"
          alt="Health care health"
          src={progressImage}
        />
        <div className="div-progress-text">
          <div className="label">MD simulation in progress</div>
          <p className="description">
            Your target metrics will be visible once the process is done.
          </p>
          <div className="div-progress">
            <ProgressBarTrack className="progress-bar-track-item" progress={progerss} />
            <div className="text-wrapper">{handleProgressNum(progerss)}</div>
          </div>
        </div>
      </div>

      <div className="frame-14">
        <div className="div-label-6">
          <div className="label-6">Downloadable files</div>
          <img className="link-3" src={HideNav} alt="img" />
        </div>
        <div className="frame-15">
          <div className="data-table-row-item">
            <DataTable
              headerData={["Name", "Format"]}
              cellData={cellData}
            />
            {/* <DataTableHeader
              cellText="Format"
              className="data-table-header-cell-item"
              resizerResizerClassName="col-3"
              size="small"
              sortable={false}
              sorted="none"
              stateProp="enabled"
            /> */}
          </div>
          {/* {cellData.map((item, index) => (
            <div className="data-table-row-item-2" key={index}>
              <div className="data-table-row">
                <DataTableRowCell
                  cellText={item[0]}
                  className="data-table-row-cell-item"
                  minHeightClassName="data-table-row-cell-instance"
                  resizerResizerClassName="col-2"
                  size="small"
                  state="enabled"
                />
                <DataTableRowCell
                  cellText={item[1]}
                  className="data-table-row-cell-item-instance"
                  minHeightClassName="col-4"
                  resizerResizerClassName="col-3"
                  size="small"
                  state="enabled"
                />
              </div>
              <div className="divider-3" />
            </div>
          ))} */}

        </div>
      </div>
    </div>
  );
};

export default ElementCreateResult;
