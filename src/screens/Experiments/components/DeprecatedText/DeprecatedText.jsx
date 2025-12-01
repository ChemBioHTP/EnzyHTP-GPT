/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { WarningAltFilled } from "../../icons/WarningAltFilled";
import { WarningFilled1 } from "../../icons/WarningFilled1";
import { StatusIcon } from "../StatusIcon";
import { useState } from "react";
import "./style.css";

export const DeprecatedText = ({
  initialInputText = "",
  size,
  className,
  textOverflowClassName,
  divClassName,
  hasIcon = true,
  backgroundClassName,
  visible = true,
  statusIconIcon = <WarningAltFilled className="icon-instance-node" color="#F1C21B" />,
  override = <WarningFilled1 className="icon-instance-node" color="#DA1E28" />,
  visible1 = true,
  onChange,
}) => {
  const [inputText, setInputText] = useState("");
  const handleInputChange = (e) => {
    setInputText(e.target.value);
    if (onChange) {
      onChange(e.target.value);
    }
  };

  return (
    <div className={`DEPRECATED-text ${size} ${className}`}>
      <div className={`text-overflow ${textOverflowClassName}`}>
        <div className={`input-text ${divClassName}`}>
        <input
            className="input-class"
            type="text"
            value={inputText}
            onChange={handleInputChange}
            placeholder={initialInputText}
          />
        </div>
      </div>
      {hasIcon && (
        <div className="icon">
          {visible && (
            <StatusIcon className="status-icon-instance" highContrast={false} icon={override} state="warning-red" />
          )}

          {visible1 && (
            <StatusIcon
              className="status-icon-instance"
              highContrast={false}
              icon={statusIconIcon}
              state="warning-yellow"
            />
          )}
        </div>
      )}

      <div className={`background ${backgroundClassName}`} />
    </div>
  );
};

DeprecatedText.propTypes = {
  inputText: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  hasIcon: PropTypes.bool,
  visible: PropTypes.bool,
  visible1: PropTypes.bool,
  onChange: PropTypes.func, // Prop for handling input text changes
};
