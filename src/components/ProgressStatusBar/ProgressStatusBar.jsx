/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { StatusIcon } from "../../screens/Experiments/components/StatusIcon";
import "./style.css";
import "../../content/general.css";

export const ProgressStatusBar = ({
  text = "Filename.png",
  size,
  state,
  className,
}) => {

  return (
    <div className={`progress-status-bar ${state} ${className}`} >
      <div className={`status-div size-${size}`}>
        <div className="status-text">{text}</div>
        {state === "success" && (
          <StatusIcon className="status-icon-instance" highContrast={false} state="success-blue" />
        )}
        {state === "error" && (
          <StatusIcon className="status-icon-instance" highContrast={false} state="error" />
        )}
      </div>
    </div>
  );
};

ProgressStatusBar.propTypes = {
  longDesc: PropTypes.string,
  shortDesc: PropTypes.string,
  fileName: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  stateProp: PropTypes.oneOf(["success", "loading", "uploaded", "error"]),
};
