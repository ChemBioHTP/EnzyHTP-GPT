/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Add1 } from "../../icons/Add1";
import { Add11 } from "../../icons/Add11";
import { Add } from "../Add";
import "./style.css";

export const Button = ({
  icon = true,
  resizer = false,
  buttonText = "Button",
  format,
  type,
  size,
  stateProp,
  className,
  iconClassName,
  override = <Add1 className="add-1" color="white" />,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    format: format || "primary",
    type: type || "text-icon",
    size: size || "large",
    state: stateProp || "enabled",
  });

  return (
    <button
      className={`button state-8-${state.state} ${state.format} size-2-${state.size} ${state.type} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
    >
      {((state.size === "expressive" && state.state === "hover") ||
        (state.size === "extra-large" && state.state === "hover") ||
        (state.size === "large" && state.state === "hover") ||
        (state.size === "medium" && state.state === "hover" && state.format === "danger-ghost") ||
        (state.size === "medium" && state.state === "hover" && state.format === "danger-tertiary") ||
        (state.size === "medium" && state.state === "hover" && state.format === "ghost") ||
        (state.size === "medium" && state.state === "hover" && state.format === "primary") ||
        (state.size === "medium" && state.state === "hover" && state.format === "secondary") ||
        (state.size === "medium" && state.state === "hover" && state.format === "tertiary") ||
        (state.size === "small" && state.state === "hover") ||
        (state.size === "two-x-large" && state.state === "hover") ||
        state.state === "active" ||
        state.state === "disabled" ||
        state.state === "enabled" ||
        state.state === "focus") && (
        <div className="button-content">
          {state.type === "text-icon" && <div className="text-wrapper">{buttonText}</div>}

          {state.type === "icon-only" && ["primary", "secondary", "tertiary"].includes(state.format) && (
            <div className="icon">
              <Add1
                className={`${["extra-large", "large", "medium", "small"].includes(state.size) && "add-1"} ${
                  state.size === "expressive" && "add-11"
                }`}
                color={
                  state.format === "tertiary" && state.state === "enabled"
                    ? "#0F62FE"
                    : state.state === "disabled" && ["primary", "secondary"].includes(state.format)
                    ? "#8D8D8D"
                    : state.format === "tertiary" && state.state === "disabled"
                    ? "#C6C6C6"
                    : "white"
                }
              />
            </div>
          )}

          {state.size === "two-x-large" && state.format === "ghost" && <div className="icon-spacer" />}

          {(state.format === "danger-ghost" ||
            state.format === "danger-primary" ||
            state.format === "danger-tertiary" ||
            state.format === "ghost" ||
            (state.format === "primary" && state.type === "text-icon") ||
            (state.format === "secondary" && state.type === "text-icon") ||
            (state.format === "tertiary" && state.type === "text-icon")) && (
            <>
              <>
                {icon && (
                  <div
                    className={`icon-3 ${
                      ["danger-primary", "danger-tertiary", "primary", "secondary", "tertiary"].includes(state.format)
                        ? iconClassName
                        : undefined
                    }`}
                  >
                    {((state.size === "expressive" && state.format === "primary") ||
                      (state.size === "expressive" && state.format === "secondary") ||
                      (state.size === "expressive" && state.format === "tertiary") ||
                      (state.size === "extra-large" && state.format === "primary") ||
                      (state.size === "extra-large" && state.format === "secondary") ||
                      (state.size === "extra-large" && state.format === "tertiary") ||
                      (state.size === "large" && state.format === "primary") ||
                      (state.size === "large" && state.format === "secondary") ||
                      (state.size === "large" && state.format === "tertiary") ||
                      (state.size === "medium" && state.format === "primary") ||
                      (state.size === "medium" && state.format === "secondary") ||
                      (state.size === "medium" && state.format === "tertiary") ||
                      (state.size === "small" && state.format === "primary") ||
                      (state.size === "small" && state.format === "secondary") ||
                      (state.size === "small" && state.format === "tertiary") ||
                      state.size === "two-x-large" ||
                      state.format === "danger-primary" ||
                      state.format === "danger-tertiary") && (
                      <>
                        <>
                          {icon && (
                            <>
                              <>
                                {["danger-primary", "danger-tertiary", "primary", "secondary", "tertiary"].includes(
                                  state.format
                                ) && <>{override}</>}

                                {state.format === "ghost" && (
                                  <Add1
                                    className="add-1"
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

                    {((state.size === "extra-large" && state.state === "disabled" && state.type === "icon-only") ||
                      (state.size === "large" && state.state === "disabled" && state.type === "icon-only") ||
                      (state.size === "medium" && state.state === "disabled" && state.type === "icon-only") ||
                      (state.size === "small" && state.state === "disabled" && state.type === "icon-only") ||
                      (state.state === "active" && state.type === "icon-only") ||
                      (state.state === "enabled" && state.type === "icon-only") ||
                      (state.state === "focus" && state.type === "icon-only") ||
                      (state.state === "hover" && state.type === "icon-only")) && (
                      <Add1
                        className={`${state.size === "expressive" ? "add-11" : "add-1"}`}
                        color={state.state === "disabled" ? "#C6C6C6" : "#161616"}
                      />
                    )}

                    {state.type === "icon-only" && state.state === "disabled" && state.size === "expressive" && (
                      <Add11 className="add-11" />
                    )}
                  </div>
                )}
              </>
            </>
          )}

          {((state.size === "expressive" && state.format === "ghost" && state.type === "text-icon") ||
            (state.size === "extra-large" && state.format === "ghost" && state.type === "text-icon") ||
            (state.size === "large" && state.format === "ghost" && state.type === "text-icon") ||
            (state.size === "medium" && state.format === "ghost" && state.type === "text-icon") ||
            (state.size === "small" && state.format === "ghost" && state.type === "text-icon") ||
            state.format === "danger-ghost") && (
            <>
              <>
                {icon && (
                  <div className="add-wrapper">
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
                            <Add1
                              className={`${state.size === "expressive" ? "add-11" : "add-1"}`}
                              color={
                                state.format === "ghost" && ["enabled", "focus"].includes(state.state)
                                  ? "#0F62FE"
                                  : state.state === "disabled"
                                  ? "#C6C6C6"
                                  : state.state === "enabled" && state.format === "danger-ghost"
                                  ? "#DA1E28"
                                  : state.format === "ghost" && ["active", "hover"].includes(state.state)
                                  ? "#0043CE"
                                  : "white"
                              }
                            />
                          )}

                          {state.state === "disabled" && state.size === "expressive" && <Add11 className="add-11" />}
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

      {state.format === "danger-primary" && state.state === "hover" && state.size === "medium" && (
        <>
          <button className="button-wrapper">
            <div className="text-wrapper-2">{buttonText}</div>
          </button>
          <>{icon && <div className="icon-2">{icon && <Add />}</div>}</>
          <>{icon && <div className="icon-2">{icon && <Add />}</div>}</>
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
