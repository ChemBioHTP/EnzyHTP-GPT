/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Add1 } from "../../screens/Login/icons/Add1";
import { Add11 } from "../../screens/Login/icons/Add11";
import { Add } from "../../screens/Login/components/Add";
import "../../content/general.css";
import "./style.css";


export const Button = ({
  icon = true,
  disabled = false,
  buttonText = "Button",
  format,
  type,
  size,
  stateProp,
  className,
  iconClassName,
  override,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    format: format || "primary",
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
        className={`button-${state.format} ${className}`}
        onMouseEnter={() => {
          dispatch(disabled? "button_disabled": "mouse_enter");
        }}
        onMouseLeave={() => {
          dispatch(disabled? "button_disabled": "mouse_leave");
        }}
        disabled = {disabled}
      >
        <div class="button-content">
          {type==="text-icon"&&(<>{buttonText}</>)}
          {icon&&(<div className="button-icon">{override}</div>)}
        </div>
      </button>
    </>
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
  format: PropTypes.oneOf([
    "danger-ghost",
    "tertiary",
    "danger-primary",
    "secondary",
    "primary",
    "danger-tertiary",
    "ghost",
  ]),
  type: PropTypes.oneOf(["icon-only", "text-icon"]),
  size: PropTypes.oneOf(["large", "two-x-large", "extra-large", "expressive", "small", "medium"]),
  stateProp: PropTypes.oneOf(["active", "enabled", "focus", "hover", "skeleton", "disabled"]),
};
