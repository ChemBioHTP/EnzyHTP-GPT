/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const ModalPanel = ({ className }) => {
  return (
    <div className={`modal-panel ${className}`}>
      <div className="tag">
        <div className="label">
          <p className="p">Give me all mutants from mutating all residue within X from Y to smaller residue</p>
        </div>
      </div>
      <div className="tag">
        <div className="label">
          <p className="p">Please give me N totally random mutations</p>
        </div>
      </div>
      <div className="tag-2">
        <div className="label-wrapper">
          <p className="p">
            Please generate N random mutants from mutating one of the residue X, Y, Z to larger residues
          </p>
        </div>
      </div>
    </div>
  );
};
