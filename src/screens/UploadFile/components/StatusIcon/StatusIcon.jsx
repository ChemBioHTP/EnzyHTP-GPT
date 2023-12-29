/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { CheckmarkFilled3 } from "../../icons/CheckmarkFilled3";
import "./style.css";

export const StatusIcon = ({
  state,
  highContrast,
  className,
  icon = <CheckmarkFilled3 className="checkmark-filled-3" color="#0F62FE" />,
}) => {
  return (
    <div className={`status-icon ${className}`}>
      <div className="overlap-group">
        <div className={`fill state-0-${state} high-contrast-${highContrast}`} />
        {icon}
      </div>
    </div>
  );
};

StatusIcon.propTypes = {
  state: PropTypes.oneOf(["success-blue", "info", "success-green", "warning-yellow", "warning-red", "error"]),
  highContrast: PropTypes.bool,
};
