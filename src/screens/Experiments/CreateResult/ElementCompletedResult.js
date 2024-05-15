import React, { useEffect, useState } from "react";
import { NavigationPage } from "../components/NavigationPage";
import { TabsItems } from "../components/TabsItems";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import "./style.css";
import "./completed.css";
import { useNavigate } from "react-router-dom";
import { ProgressBarTrack } from "../components/ProgressBarTrack";
import efImage from "../../../assets/images/Experiments/ElementCreateResult/coarse_ef_dist_kde.png";
import stabilityImage from "../../../assets/images/Experiments/ElementCreateResult/coarse_stab_dist_kde.png";
import downloadIcon from "../../../assets/images/Experiments/hide-nav.svg";
import { Checkbox } from "../../../assets/icons/Checkbox";

export const ElementCompletedResult = ({
  sideVisible = true,
  titleText = "My awesome experiment",
  onClickWrapper = () => {},
}) => {
  const handleWrapperClick = (id) => {
    onClickWrapper(id);
  };

  useEffect(() => {
    if (sideVisible) {
      document.body.style.setProperty("--result-left-distance", "0px");
    } else {
      document.body.style.setProperty("--result-left-distance", "-214px");
    }
  }, [sideVisible]);

  let navigate = useNavigate();

  const handleBackToList = () => {
    let path = "/exp";
    navigate(path);
  };

  return (
    <div>
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
      </div>

      <div className="workspace">
        <div className="matrics-title title">
          <span>Target Matrics</span>
          <img className="download-icon" src={downloadIcon} />
        </div>
        <div className="download-title title">
          <span>Downloadable Files</span>
          <img className="download-icon" src={downloadIcon} />
        </div>
        <table className="download-table">
          <thead>
            <tr className="table-header">
              <th>Name</th>
              <th>Format</th>
            </tr>
          </thead>
          <tbody>
            <tr className="table-row">
              <td>WT structure (fixed)</td>
              <td>.pdb</td>
            </tr>
            <tr className="table-row">
              <td>MD instruction file</td>
              <td>.in</td>
            </tr>
            <tr className="table-row">
              <td>MD constraint file</td>
              <td>.rs</td>
            </tr>
            <tr className="table-row">
              <td>MD trajectory files</td>
              <td>.zip</td>
            </tr>
          </tbody>
        </table>

        <div className="dist-kde">
          <img src={efImage} />
          <img src={stabilityImage} />
        </div>
        <table className="mutations">
          <thead>
            <tr className="table-header">
              <th>Number</th>
              <th>Pattern</th>
              <th>EF (MV/cm)</th>
              <th>SPI</th>
              <th>Stability</th>
            </tr>
          </thead>
          <tbody>
            <tr className="table-row">
              <td>01</td>
              <td>NA22K EA24K KA162L RA163L</td>
              <td>3.144062</td>
              <td>1.561</td>
              <td>-2.25</td>
            </tr>
            <tr className="table-row">
              <td>02</td>
              <td>NA22R SA29K EA24Q KA162I RA163F</td>
              <td>2.746778</td>
              <td>1.308</td>
              <td>-0.30</td>
            </tr>
            <tr className="table-row">
              <td>02</td>
              <td>NA22K SA29K EA24V KA162D RA163F</td>
              <td>2.285668</td>
              <td>1.427</td>
              <td>1.83</td>
            </tr>
            <tr className="table-row">
              <td>02</td>
              <td>SA29K EA24Q KA162D RA163L</td>
              <td>1.540748</td>
              <td>1.654</td>
              <td>-0.10</td>
            </tr>
            <tr className="table-row">
              <td>02</td>
              <td>WT</td>
              <td>-4.458684</td>
              <td>1.486</td>
              <td>0.0</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ElementCompletedResult;
