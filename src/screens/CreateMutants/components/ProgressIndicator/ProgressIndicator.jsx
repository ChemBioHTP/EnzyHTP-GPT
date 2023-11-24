/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { TooltipItem } from "../TooltipItem";
import "./style.css";

export const ProgressIndicator = ({ stepText = "Step", stateProp, tooltip, className }) => {
  const [state, dispatch] = useReducer(reducer, {
    state: stateProp || "enabled",
    tooltip: tooltip || false,
  });

  return (
    <div
      className={`progress-indicator state-21-${state.state} ${className}`}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
    >
      {!state.tooltip && <div className="step-label">{stepText}</div>}

      {state.state === "tooltip" && (
        <>
          <div className="step-label-wrapper">
            <div className="step-label-2">{stepText}</div>
          </div>
          <div className="tooltip-overflow">
            <TooltipItem
              alignment="center"
              className="tooltip-item-instance"
              position="top"
              tooltipText="Tooltip text"
              type="icon"
            />
          </div>
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  switch (action) {
    case "mouse_enter":
      return {
        ...state,
        state: "hover",
      };

    case "mouse_leave":
      return {
        ...state,
        state: "enabled",
      };
  }

  return state;
}

ProgressIndicator.propTypes = {
  stepText: PropTypes.string,
  stateProp: PropTypes.oneOf(["active", "enabled", "focus", "tooltip", "hover", "disabled"]),
  tooltip: PropTypes.bool,
};
