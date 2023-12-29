/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { StatusIcon } from "../StatusIcon";
import "./style.css";

export const DeprecatedText = ({
  inputText = "Input text",
  size,
  className,
  textOverflowClassName,
  divClassName,
  hasIcon = true,
  backgroundClassName,
  visible = true,
  visible1 = true,
}) => {
  return (
    <div className={`DEPRECATED-text size-22-${size} ${className}`}>
      <div className={`text-overflow ${textOverflowClassName}`}>
        <div className={`input-text ${divClassName}`}>{inputText}</div>
      </div>
      {hasIcon && (
        <div className="icon-3">
          {visible && <StatusIcon className="status-icon-instance" highContrast={false} state="warning-red" />}

          {visible1 && <StatusIcon className="status-icon-instance" highContrast={false} state="warning-yellow" />}
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
};
