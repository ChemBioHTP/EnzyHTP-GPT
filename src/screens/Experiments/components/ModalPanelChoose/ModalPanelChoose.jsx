/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React, { useState } from "react";
import { IconEdit3 } from "../../icons/IconEdit3";
import { Checkbox } from "../Checkbox";
import "./style.css";
import { Tile } from "../Tile";

export const ModalPanelChoose = ({ className, onClickEidt = () => { } }) => {
  const handleClickEidt = (value) => {
    onClickEidt(value);
  }

  const [checked, setChecked] = useState(false);

  const handleCheckboxChange = () => {
    setChecked(prev => !prev);
  };

  const [tileSelected1, setTileSelected1] = useState(false);
  const [tileSelected2, setTileSelected2] = useState(true);
  const handleTileChange = (value) => {
    if (value === 1) {
      setTileSelected1(true);
      setTileSelected2(false);
    } else {
      setTileSelected2(true);
      setTileSelected1(false);
    }
  };

  return (
    <div className={`modal-panel-choose ${className}`}>
      <div className="frame">
        <Tile
          titleText="Let Our System Handle It"
          className="tile-instance"
          descText="Ideal if you don't have a service or prefer convenience. May take longer."
          type="single-select"
          stateProp={tileSelected1?"selected":"enabled"}
          onClick={()=>handleTileChange(1)}
        />
        <Tile
          titleText="Run MD Simulation Yourself"
          className="tile-instance"
          descText="Ideal if you have your own tool or service to run the MD simulation."
          type="single-select"
          stateProp={tileSelected2?"selected":"enabled"}
          onClick={()=>handleTileChange(2)}
        />
      </div>
      {/* <div className="text-wrapper-4">
        <input
          type="checkbox"
          className="custom-checkbox"
          checked={checked}
          onChange={handleCheckboxChange}
        />
        Set as default. You won't be prompted again, but you can adjust this in the experiment settings.
      </div> */}
    </div>
  );
};
