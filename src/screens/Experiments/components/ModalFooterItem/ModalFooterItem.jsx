/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Button } from "../Button";
import "./style.css";

export const ModalFooterItem = ({
  actions,
  cancel,
  className,
  buttonButtonText = "Button",
  buttonButtonText1 = "Button",
  onClick=()=>{},
}) => {
  const handleButtonClick = (id) => {
    onClick(id);
  }
  return (
    <div className={`modal-footer-item ${className}`}>
      {((cancel && actions === "one") || (!cancel && actions === "two")) && (
        <>

          <Button
            buttonText={actions === "one" ? "Cancel" : buttonButtonText}
            className="instance-node"
            divClassName={`${actions === "two" && "button-instance"}`}
            divClassNameOverride={`${actions === "one" && "button-instance"}`}
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style={actions === "one" ? "ghost" : "secondary"}
            type="text-icon"
            onClick={()=>handleButtonClick(0)}
          />

          <Button
            buttonText={buttonButtonText1}
            className="instance-node1"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style="primary"
            type="text-icon"
            onClick={()=>handleButtonClick(1)}
          />

        </>
      )}

      {!cancel && ["one", "three"].includes(actions) && (
        <>
          <div className="spacer" />
          <Button
            buttonText={actions === "three" ? "Button" : buttonButtonText1}
            className="instance-node"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style={actions === "three" ? "secondary" : "primary"}
            type="text-icon"
          />
        </>
      )}

      {actions === "three" && !cancel && (
        <>
          <Button
            buttonText={buttonButtonText}
            className="instance-node"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style="secondary"
            type="text-icon"
            onClick={()=>handleButtonClick(0)}
          />
          <Button
            buttonText={buttonButtonText1}
            className="instance-node"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style="primary"
            type="text-icon"
            onClick={()=>handleButtonClick(1)}
          />
        </>
      )}

      {cancel && ["three", "two"].includes(actions) && (
        <Button
          buttonText="Cancel"
          className="instance-node"
          divClassNameOverride="button-instance"
          icon={false}
          size="extra-large"
          stateProp="enabled"
          style="ghost"
          type="text-icon"
          onClick={()=>handleButtonClick(0)}
        />
      )}

      {cancel && actions === "two" && <div className="spacer" />}

      {cancel && ["three", "two"].includes(actions) && (
        <>
          <Button
            buttonText={actions === "three" ? "Button" : buttonButtonText}
            className="instance-node"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style="secondary"
            type="text-icon"
            onClick={()=>handleButtonClick(0)}
          />
          <Button
            buttonText={actions === "three" ? buttonButtonText : buttonButtonText1}
            className="instance-node"
            divClassName="button-instance"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style={actions === "three" ? "secondary" : "primary"}
            type="text-icon"
            onClick={()=>handleButtonClick(1)}
          />
        </>
      )}

      {cancel && actions === "three" && (
        <Button
          buttonText={buttonButtonText1}
          className="instance-node"
          divClassName="button-instance"
          icon={false}
          size="extra-large"
          stateProp="enabled"
          style="primary"
          type="text-icon"
          onClick={()=>handleButtonClick(1)}
        />
      )}
    </div>
  );
};

ModalFooterItem.propTypes = {
  actions: PropTypes.oneOf(["two", "three", "one"]),
  cancel: PropTypes.bool,
  buttonButtonText: PropTypes.string,
  buttonButtonText1: PropTypes.string,
};
