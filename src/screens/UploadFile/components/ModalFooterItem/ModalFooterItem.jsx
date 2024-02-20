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
  buttonStateProp = "enabled",
  buttonButtonText1 = "Button",
}) => {
  return (
    <div className={`modal-footer-item ${className}`}>
      {((cancel && actions === "one") || (!cancel && actions === "two")) && (
        <>
          <Button
            buttonText={actions === "one" ? "Cancel" : buttonButtonText}
            className="button-3"
            divClassName={`${actions === "two" && "button-4"}`}
            divClassNameOverride={`${actions === "one" && "button-4"}`}
            icon={false}
            size="extra-large"
            stateProp="enabled"
            style={actions === "one" ? "ghost" : "secondary"}
            type="text-icon"
          />
          <Button
            buttonText={buttonButtonText1}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp={buttonStateProp}
            type="text-icon"
          />
        </>
      )}

      {!cancel && ["one", "three"].includes(actions) && (
        <>
          <div className="spacer" />
          <Button
            buttonText={actions === "three" ? "Button" : buttonButtonText1}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp={actions === "three" ? "enabled" : buttonStateProp}
            style={actions === "three" ? "secondary" : "primary"}
            type="text-icon"
          />
        </>
      )}

      {actions === "three" && !cancel && (
        <>
          <Button
            buttonText={buttonButtonText}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            type="text-icon"
          />
          <Button
            buttonText={buttonButtonText1}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp={buttonStateProp}
            type="text-icon"
          />
        </>
      )}

      {cancel && ["three", "two"].includes(actions) && (
        <Button
          buttonText="Cancel"
          className="button-3"
          divClassNameOverride="button-4"
          icon={false}
          size="extra-large"
          stateProp="enabled"
          type="text-icon"
        />
      )}

      {cancel && actions === "two" && <div className="spacer" />}

      {cancel && ["three", "two"].includes(actions) && (
        <>
          <Button
            buttonText={actions === "three" ? "Button" : buttonButtonText}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp="enabled"
            type="text-icon"
          />
          <Button
            buttonText={actions === "three" ? buttonButtonText : buttonButtonText1}
            className="button-3"
            divClassName="button-4"
            icon={false}
            size="extra-large"
            stateProp={actions === "three" ? "enabled" : buttonStateProp}
            style={actions === "three" ? "secondary" : "primary"}
            type="text-icon"
          />
        </>
      )}

      {cancel && actions === "three" && (
        <Button
          buttonText={buttonButtonText1}
          className="button-3"
          divClassName="button-4"
          icon={false}
          size="extra-large"
          stateProp={buttonStateProp}
          type="text-icon"
        />
      )}
    </div>
  );
};

ModalFooterItem.propTypes = {
  actions: PropTypes.oneOf(["two", "three", "one"]),
  cancel: PropTypes.bool,
  buttonButtonText: PropTypes.string,
  buttonStateProp: PropTypes.string,
  buttonButtonText1: PropTypes.string,
};
