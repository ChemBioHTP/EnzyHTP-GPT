/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { IconEdit3 } from "../../icons/IconEdit3";
import { Checkbox } from "../Checkbox";
import "./style.css";

export const ModalPanelMetrics = ({ className, onClickEidt = () => { } }) => {
  const handleClickEidt = (value) => {
    onClickEidt(value);
  }
  return (
    <div className={`modal-panel-metrics ${className}`}>
      <div className="frame">
        <div className="frame-2">
          <div className="frame-3">
            <Checkbox
              className="checkbox-instance"
              label={false}
              selection="unchecked"
              stateProp="enabled"
              value={false}
            />
            <div className="text-wrapper-2">EF</div>
          </div>
          <div className="text-wrapper-3">{""}</div>
        </div>
        <IconEdit3 className="icon-edit" color="#0F62FE" onClick={()=>handleClickEidt(0)}/>
      </div>
      <div className="frame">
        <div className="frame-2">
          <div className="frame-3">
            <Checkbox
              className="checkbox-instance"
              label={false}
              selection="checked"
              stateProp="enabled"
              value={false}
            />
            <div className="text-wrapper-2">SPI</div>
          </div>
          <div className="text-wrapper-4">pocket: default, substrate: default</div>
        </div>
        <IconEdit3 className="icon-edit" color="#0F62FE" onClick={()=>handleClickEidt(1)}/>
      </div>
      <div className="frame">
        <div className="frame-2">
          <div className="frame-3">
            <Checkbox
              className="checkbox-instance"
              label={false}
              selection="checked"
              stateProp="enabled"
              value={false}
            />
            <div className="text-wrapper-2">RMSD</div>
          </div>
          <div className="text-wrapper-3">ligand: default</div>
        </div>
        <IconEdit3 className="icon-edit" color="#0F62FE" onClick={()=>handleClickEidt(2)}/>
      </div>
      <div className="frame">
        <div className="frame-2">
          <div className="frame-3">
            <Checkbox
              className="checkbox-instance"
              label={false}
              selection="checked"
              stateProp="enabled"
              value={false}
            />
            <div className="text-wrapper-2">MMPBSA</div>
          </div>
          <div className="text-wrapper-3">ligand: default</div>
        </div>
        <IconEdit3 className="icon-edit" color="#0F62FE" onClick={()=>handleClickEidt(3)}/>
      </div>
      <div className="frame">
        <div className="frame-2">
          <div className="frame-3">
            <Checkbox
              className="checkbox-instance"
              label={false}
              selection="checked"
              stateProp="enabled"
              value={false}
            />
            <div className="text-wrapper-2">Stability</div>
          </div>
        </div>
        <IconEdit3 className="icon-edit" color="#0F62FE" onClick={()=>handleClickEidt(4)}/>
      </div>
    </div>
  );
};
