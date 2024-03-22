/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { ToggleSwitchSmall } from "../ToggleSwitchSmall";
import "./style.css";

export const ToggleItem = ({ size, state, className }) => {
  return (
    <div className={`toggle-item ${state} ${size} ${className}`}>
      {size === "default" && <div className="switch" />}

      {size === "small" && <ToggleSwitchSmall disabled={false} toggled={false} />}
    </div>
  );
};

ToggleItem.propTypes = {
  size: PropTypes.oneOf(["small", "default"]),
  state: PropTypes.oneOf(["read-only", "enabled"]),
};
