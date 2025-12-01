/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { CheckmarkFilled } from "../../icons/CheckmarkFilled";
import { ErrorFilled } from "../../icons/ErrorFilled";
import { InformationFilled } from "../../icons/InformationFilled";
import { WarningAltFilled } from "../../icons/WarningAltFilled";
import { WarningFilled } from "../../icons/WarningFilled";
import "./style.css";

export const StatusIcon = ({ state, highContrast, className }) => {
  return (
    <div className={`status-icon ${className}`}>
      <div className="overlap-group">
        <div className={`fill ${state} high-contrast-${highContrast}`} />
        {["success-blue", "success-green"].includes(state) && (
          <CheckmarkFilled
            className="instance-node-4"
            color={
              state === "success-green" && highContrast
                ? "#42BE65"
                : state === "success-blue" && !highContrast
                ? "#0F62FE"
                : state === "success-blue" && highContrast
                ? "#4589FF"
                : "#24A148"
            }
          />
        )}

        {state === "info" && (
          <InformationFilled className="instance-node-4" color={!highContrast ? "#0043CE" : "#4589FF"} />
        )}

        {state === "warning-yellow" && !highContrast && <WarningAltFilled className="instance-node-4" />}

        {state === "error" && <ErrorFilled className="instance-node-4" color={highContrast ? "#FA4D56" : "#DA1E28"} />}

        {(state === "warning-red" || (highContrast && state === "warning-yellow")) && (
          <WarningFilled
            className="instance-node-4"
            color={!highContrast ? "#DA1E28" : state === "warning-yellow" ? "#F1C21B" : "#FA4D56"}
          />
        )}
      </div>
    </div>
  );
};

StatusIcon.propTypes = {
  state: PropTypes.oneOf(["success-blue", "info", "success-green", "warning-yellow", "warning-red", "error"]),
  highContrast: PropTypes.bool,
};
