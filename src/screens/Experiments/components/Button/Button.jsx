/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Add } from "../../icons/Add";
import { Add10 } from "../../icons/Add10";
import { AddWrapper } from "../AddWrapper";
import "./style.css";

export const Button = ({
  icon = true,
  resizer = false,
  buttonText = "Button",
  disabled = false,
  style,
  type,
  size,
  stateProp,
  className,
  override = <Add className="add-56" color="#161616" />,
  iconClassName,
  icon1 = <Add className="add-56" color="#FFFFFF" />,
  onClick,
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
    <button
      className={`button ${state.state} ${state.style} ${state.size} ${state.type} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onClick={onClick}
    >
      {((state.size === "expressive" && state.state === "hover") ||
        (state.size === "extra-large" && state.state === "hover") ||
        (state.size === "large" && state.state === "hover") ||
        (state.size === "medium" && state.state === "hover" && state.style === "danger-ghost") ||
        (state.size === "medium" && state.state === "hover" && state.style === "danger-tertiary") ||
        (state.size === "medium" && state.state === "hover" && state.style === "ghost") ||
        (state.size === "medium" && state.state === "hover" && state.style === "primary") ||
        (state.size === "medium" && state.state === "hover" && state.style === "secondary") ||
        (state.size === "medium" && state.state === "hover" && state.style === "tertiary") ||
        (state.size === "small" && state.state === "hover") ||
        (state.size === "two-x-large" && state.state === "hover") ||
        state.state === "active" ||
        state.state === "disabled" ||
        state.state === "enabled" ||
        state.state === "focus") && (
        <div className="button-content">
          {state.type === "text-icon" && <div className="text-wrapper-2">{buttonText}</div>}

          {state.type === "icon-only" && ["primary", "secondary", "tertiary"].includes(state.style) && (
            <div className="add-wrapper">{override}</div>
          )}

          {state.size === "two-x-large" && state.style === "ghost" && <div className="icon-spacer" />}

          {(state.style === "danger-ghost" ||
            state.style === "danger-primary" ||
            state.style === "danger-tertiary" ||
            state.style === "ghost" ||
            (state.style === "primary" && state.type === "text-icon") ||
            (state.style === "secondary" && state.type === "text-icon") ||
            (state.style === "tertiary" && state.type === "text-icon")) && (
            <>
              <>
                {icon && (
                  <div
                    className={`icon-4 ${
                      ["danger-primary", "danger-tertiary", "primary", "secondary", "tertiary"].includes(state.style)
                        ? iconClassName
                        : undefined
                    }`}
                  >
                    {((state.size === "expressive" && state.style === "primary") ||
                      (state.size === "expressive" && state.style === "secondary") ||
                      (state.size === "expressive" && state.style === "tertiary") ||
                      (state.size === "extra-large" && state.style === "primary") ||
                      (state.size === "extra-large" && state.style === "secondary") ||
                      (state.size === "extra-large" && state.style === "tertiary") ||
                      (state.size === "large" && state.style === "primary") ||
                      (state.size === "large" && state.style === "secondary") ||
                      (state.size === "large" && state.style === "tertiary") ||
                      (state.size === "medium" && state.style === "primary") ||
                      (state.size === "medium" && state.style === "secondary") ||
                      (state.size === "medium" && state.style === "tertiary") ||
                      (state.size === "small" && state.style === "primary") ||
                      (state.size === "small" && state.style === "secondary") ||
                      (state.size === "small" && state.style === "tertiary") ||
                      state.size === "two-x-large" ||
                      state.style === "danger-primary" ||
                      state.style === "danger-tertiary") && (
                      <>
                        <>
                          {icon && (
                            <>
                              <>
                                {["danger-primary", "danger-tertiary", "primary", "secondary", "tertiary"].includes(
                                  state.style
                                ) && <>{icon1}</>}

                                {state.style === "ghost" && (
                                  <Add
                                    className="add-56"
                                    color={
                                      state.state === "disabled"
                                        ? "#C6C6C6"
                                        : ["active", "hover"].includes(state.state)
                                        ? "#0043CE"
                                        : "#0F62FE"
                                    }
                                  />
                                )}
                              </>
                            </>
                          )}
                        </>
                      </>
                    )}

                    {state.type === "icon-only" && <>{override}</>}
                  </div>
                )}
              </>
            </>
          )}

          {((state.size === "expressive" && state.style === "ghost" && state.type === "text-icon") ||
            (state.size === "extra-large" && state.style === "ghost" && state.type === "text-icon") ||
            (state.size === "large" && state.style === "ghost" && state.type === "text-icon") ||
            (state.size === "medium" && state.style === "ghost" && state.type === "text-icon") ||
            (state.size === "small" && state.style === "ghost" && state.type === "text-icon") ||
            state.style === "danger-ghost") && (
            <>
              <>
                {icon && (
                  <div className="icon-2">
                    {icon && (
                      <>
                        <>
                          {((state.size === "extra-large" && state.state === "disabled") ||
                            (state.size === "large" && state.state === "disabled") ||
                            (state.size === "medium" && state.state === "disabled") ||
                            (state.size === "small" && state.state === "disabled") ||
                            state.state === "active" ||
                            state.state === "enabled" ||
                            state.state === "focus" ||
                            state.state === "hover") && (
                            <Add
                              className={`${state.size === "expressive" ? "add-10" : "add-56"}`}
                              color={
                                state.style === "ghost" && ["enabled", "focus"].includes(state.state)
                                  ? "#0F62FE"
                                  : state.state === "disabled"
                                  ? "#C6C6C6"
                                  : state.state === "enabled" && state.style === "danger-ghost"
                                  ? "#DA1E28"
                                  : state.style === "ghost" && ["active", "hover"].includes(state.state)
                                  ? "#0043CE"
                                  : "white"
                              }
                            />
                          )}

                          {state.state === "disabled" && state.size === "expressive" && <Add10 className="add-10" />}
                        </>
                      </>
                    )}
                  </div>
                )}
              </>
            </>
          )}
        </div>
      )}

      {state.style === "danger-primary" && state.state === "hover" && state.size === "medium" && (
        <>
          <button className="button-wrapper">
            <div className="text-wrapper-3">{buttonText}</div>
          </button>
          <>{icon && <div className="icon-3">{icon && <AddWrapper />}</div>}</>
          <>{icon && <div className="icon-3">{icon && <AddWrapper />}</div>}</>
        </>
      )}
    </button>
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
  style: PropTypes.oneOf([
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
