import React from "react";
import { ModalFooterItem } from "../components/ModalFooterItem";
import { ModalPanelWorkflow } from "../components/ModalPanelWorkflow";
import { Close97 } from "../icons/Close97";
import "./style.css";
import navRock from "../../../assets/images/Experiments/navigate-rock-the-boat-1.png"

export const ElementChangeWorkFLow = ({
  title="title", 
  content="this is content", 
  slotItem, 
  onCloseClick = () => { },
  onSaveClick = () => { },
}) => {
  const handleCloseClick = () => {
    onCloseClick();
  };

  const handleBottonClick = (id) => {
    console.log(id);
    if (id == 0) {
      onCloseClick();
    } else{
      onSaveClick();
    }
  };
  return (
    <div className="workflow-change">
      <div className="div-3">
        <header className="header">
          <div className="label-title">
            <div className="text-wrapper-4">{title}</div>
          </div>
          <Close97 className="close-82" color="#161616" onClick={handleCloseClick}/>
        </header>
        <div className="content">
          <div className="text">
            <div className="subtext-margin">
              <p className="text-wrapper-5">{content}</p>
            </div>
          </div>
          <div className="slot">
            {slotItem}
          </div>
        </div>
      </div>
      <ModalFooterItem
        actions="two"
        buttonButtonText="Cancel"
        buttonButtonText1="Save"
        cancel={false}
        className="modal-footer-item-instance"
        onClick={handleBottonClick}
      />
    </div>
  );
};

export default ElementChangeWorkFLow;
