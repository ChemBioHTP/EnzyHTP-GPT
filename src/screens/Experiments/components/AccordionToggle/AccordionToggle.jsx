/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { ToggleItem } from "../ToggleItem";
import "./style.css";

export const AccordionToggle = ({ state, className }) => {
  return (
    <div className={`accordion-with ${className}`}>
      <div className="accordion-header">
        <div className="text-wrapper">Input with GUI</div>
        {state === "off" && <ToggleItem className="toggle-item-instance" size="small" state="enabled" />}

        {state === "on" && (
          <div className="toggle">
            <div className="toggle-value">
              <ToggleItem className="instance-node" size="small" state="enabled" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

AccordionToggle.propTypes = {
  state: PropTypes.oneOf(["off", "on"]),
};
