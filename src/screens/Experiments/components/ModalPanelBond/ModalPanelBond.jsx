import React from "react";
import { TextInputDefault } from "../../../../components/TextInputDefault";
import "./style.css";

export const ModalPanelBond = () => {
  const handleInputChange = (value, index) => {
    console.log(value, index);
  }
  return (
    <div className="modal-panel-bond">
      <div className="frame">
        <div className="frame-2">
          <div className="text-wrapper">Index of bond atoms</div>
          <p className="p">Specify the atom indexes that defines the bond of interest.</p>
        </div>
        <div className="frame-wrapper">
          <div className="frame-3">
            <TextInputDefault
              backgroundClassName="text-input-default-2"
              className="text-input-default-instance"
              placeholderText="int"
              showHelper={false}
              showLabel={false}
              size="large"
              spacerClassName="design-component-instance-node"
              state="enabled"
              textFilled={false}
              onInputChange={(value)=>handleInputChange(value,0)}
            />
            <TextInputDefault
              backgroundClassName="text-input-default-2"
              className="text-input-default-instance"
              placeholderText="int"
              showHelper={false}
              showLabel={false}
              size="large"
              spacerClassName="design-component-instance-node"
              state="enabled"
              textFilled={false}
              onInputChange={(value)=>handleInputChange(value,1)}
            />
          </div>
        </div>
      </div>
      <div className="frame-4" />
    </div>
  );
};
