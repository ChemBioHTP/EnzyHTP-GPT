/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import "../../content/general.css";
import "./style.css";


export const Button = ({
  icon = true,
  disabled = false,
  buttonText = "Button",
  style,
  type,
  size,
  stateProp,
  className,
  iconClassName,
  override,
  onClick
}) => {
  const [state, dispatch] = useReducer(reducer, {
    style: style || "primary",
    type: type || "text-icon",
    size: size || "large",
    state: stateProp || "enabled",
  });

  if(state.state!=="disabled" && disabled){
    dispatch("button_disabled");
  } else if (state.state === "disabled" && !disabled) {
    dispatch("button_enabled");
  }
  
  return (
    <>
      <button
        className={`button-${state.style} button-size-${state.size} button-type-${state.type} ${className}`}
        disabled={disabled}
        onClick={onClick}
      >
        <div class="button-content">
          {type==="text-icon"&&(<>{buttonText}</>)}
          {icon&&(<div className={`button-icon ${iconClassName}`}>{override}</div>)}
        </div>
      </button>
    </>
  );
};

function reducer(state, action) {
  switch (action) {
    case "button_disabled":
      return {
        ...state,
        state: "disabled",
      };
    case "button_enabled":
      return {
        ...state,
        state: "enabled",
      };
  }

  return state;
}

Button.propTypes = {
  icon: PropTypes.bool,
  resizer: PropTypes.bool,
  buttonText: PropTypes.string,
  style: PropTypes.oneOf([
    "tertiary",
    "secondary",
    "primary",
    "danger",
    "ghost",
  ]),
  type: PropTypes.oneOf(["icon-only", "text-icon"]),
  size: PropTypes.oneOf(["large", "two-x-large", "extra-large", "expressive", "small", "medium"]),
  stateProp: PropTypes.oneOf(["active", "enabled", "disabled"]),
};
