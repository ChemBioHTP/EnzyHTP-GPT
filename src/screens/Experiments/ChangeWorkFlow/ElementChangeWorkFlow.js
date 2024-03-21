import React from "react";
import { ModalFooterItem } from "../components/ModalFooterItem";
import { ModalPanelWorkflow } from "../components/ModalPanelWorkflow";
import { Close97 } from "../icons/Close97";
import "./style.css";
import navRock from "../../../assets/images/Experiments/navigate-rock-the-boat-1.png"

export const ElementChangeWorkFLow = ({ onCloseClick = () => { } }) => {
  const handleCloseClick = () => {
    onCloseClick();
  };
  return (
    <div className="workflow-change">
      <div className="div-2">
        <header className="header">
          <div className="label-title">
            <div className="text-wrapper-4">Change workflow</div>
          </div>
          <Close97 className="close-82" color="#161616" onClick={handleCloseClick}/>
        </header>
        <div className="content">
          <div className="text">
            <div className="subtext-margin">
              <p className="text-wrapper-5">Choose a workflow to determine the processes to apply to the wild type.</p>
            </div>
          </div>
          <div className="slot">
            <ModalPanelWorkflow
              backgroundClassName="modal-panel-workflow-2"
              className="modal-panel-workflow-instance"
              navigateRockThe={navRock}
            />
          </div>
        </div>
      </div>
      <ModalFooterItem
        actions="two"
        buttonButtonText="Cancel"
        buttonButtonText1="Save"
        cancel={false}
        className="modal-footer-item-instance"
      />
    </div>
  );
};

export default ElementChangeWorkFLow;
