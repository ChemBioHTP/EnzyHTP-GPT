/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Close97 } from "../../icons/Close97";
import "./style.css";

export const TagCloseButton = ({ size, color, stateProp, className, close97Color = "#150080" }) => {
  const [state, dispatch] = useReducer(reducer, {
    size: size || "medium",
    color: color || "blue",
    state: stateProp || "enabled",
  });

  return (
    <div
      className={`tag-close-button size-6-${state.size} state-5-${state.state} color-0-${state.color} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
    >
      <Close97
        className="close-97"
        color={close97Color}
        fillOpacity={state.state === "disabled" ? "0.25" : undefined}
      />
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

TagCloseButton.propTypes = {
  size: PropTypes.oneOf(["medium", "small"]),
  color: PropTypes.oneOf([
    "teal",
    "gray",
    "cool-gray",
    "outline",
    "warm-gray",
    "blue",
    "high-contrast",
    "green",
    "magenta",
    "red",
    "purple",
    "cyan",
  ]),
  stateProp: PropTypes.oneOf(["disabled", "hover", "focus", "enabled"]),
  close97Color: PropTypes.string,
};
