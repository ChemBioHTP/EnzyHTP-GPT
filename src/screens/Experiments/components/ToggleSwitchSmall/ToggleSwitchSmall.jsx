/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Checkmark1 } from "../../icons/Checkmark1";
import "./style.css";

export const ToggleSwitchSmall = ({ toggled, disabled }) => {
  return (
    <div className={`toggle-switch-small disabled-${disabled} toggled-${toggled}`}>
      {toggled && (
        <Checkmark1
          className="checkmark"
          color={disabled ? "#8D8D8D" : "#161616"}
          stroke={disabled ? "#8D8D8D" : "#24A148"}
        />
      )}
    </div>
  );
};

ToggleSwitchSmall.propTypes = {
  toggled: PropTypes.bool,
  disabled: PropTypes.bool,
};
