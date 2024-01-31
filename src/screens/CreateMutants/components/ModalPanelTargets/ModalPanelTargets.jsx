/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const ModalPanelTargets = ({ className }) => {
  return (
    <div className={`modal-panel-targets ${className}`}>
      <div className="div-wrapper">
        <div className="label-2">R101</div>
      </div>
      <div className="div-wrapper">
        <div className="label-2">R102</div>
      </div>
      <div className="div-wrapper">
        <div className="label-2">R103</div>
      </div>
    </div>
  );
};
