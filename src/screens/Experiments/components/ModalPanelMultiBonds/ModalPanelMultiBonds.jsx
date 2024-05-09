import React from "react";
import { TextInputDefault } from "../../../../components/TextInputDefault";
import { IconHelpCircle1 } from "../../icons/IconHelpCircle1";
import "./style.css";

export const ModalPanelMultiBonds = () => {
  const handleInputChange = (value, index) => {
    console.log(value, index);
  }
  return (
    <div className="modal-panel-bonds">
      <div className="frame">
        <div className="frame-2">
          <div className="text-wrapper">Substrate</div>
          <div className="frame-3">
            <p className="p">A selection pattern defined in PyMol style.</p>
            <IconHelpCircle1 className="icon-help-circle" />
          </div>
        </div>
        <div className="frame-wrapper">
          <div className="text-input-default-wrapper">
            <TextInputDefault
              backgroundClassName="text-input-default-2"
              className="text-input-default-instance"
              placeholderText="string"
              showHelper={false}
              showLabel={false}
              size="large"
              spacerClassName="design-component-instance-node"
              state="enabled"
              textFilled={false}
              onInputChange={(value)=>handleInputChange(value,0)}
            />
          </div>
        </div>
      </div>
      <div className="frame">
        <div className="frame-2">
          <div className="text-wrapper">Pocket</div>
          <p className="text-wrapper-2">A selection pattern defined in PyMol style.</p>
        </div>
        <div className="frame-wrapper">
          <div className="text-input-default-wrapper">
            <TextInputDefault
              backgroundClassName="text-input-default-2"
              className="text-input-default-instance"
              placeholderText="string"
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
      <div className="frame">
        <div className="frame-2">
          <div className="text-wrapper">Protein</div>
          <p className="text-wrapper-2">A selection pattern defined in PyMol style.</p>
        </div>
        <div className="frame-wrapper">
          <div className="text-input-default-wrapper">
            <TextInputDefault
              backgroundClassName="text-input-default-2"
              className="text-input-default-instance"
              placeholderText="string"
              showHelper={false}
              showLabel={false}
              size="large"
              spacerClassName="design-component-instance-node"
              state="enabled"
              textFilled={false}
              onInputChange={(value)=>handleInputChange(value,2)}
            />
          </div>
        </div>
      </div>
      <div className="frame-4" />
    </div>
  );
};
