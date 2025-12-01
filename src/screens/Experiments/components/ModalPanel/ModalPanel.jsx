/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React, { useState } from "react";
import "./style.css";

export const ModalPanel = ({ className, onClick = () => { } }) => {
  const handleClick = (tagItem) => {
    onClick(tagItem);
  };

  const [tagText, setTagText] = useState(["Give me all mutants from mutating all residue within X from Y to smaller residue",
    "Please give me N totally random mutations",
    "Please generate N random mutants from mutating one of the residue X, Y, Z to larger residues"]);
  return (
    <div className={`modal-panel ${className}`}>
      <div className="tag" onClick={() => handleClick(tagText[0])}>
        <div className="label">
          <p className="p">{tagText[0]}</p>
        </div>
      </div>
      <div className="tag" onClick={() => handleClick(tagText[1])}>
        <div className="label">
          <p className="p">{tagText[1]}</p>
        </div>
      </div>
      <div className="tag-2" onClick={() => handleClick(tagText[2])}>
        <div className="label-wrapper">
          <p className="p">
          {tagText[2]}
          </p>
        </div>
      </div>
    </div>
  );
};
