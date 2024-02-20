/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Bee6 } from "../../icons/Bee6";
import "./style.css";

export const TabsItems = ({
  hoverDimissible = false,
  show2NdLabel = false,
  divider = true,
  dismissibleIcon = false,
  labelText = "Tab label",
  dismissible = false,
  icon = false,
  style,
  type,
  size,
  alignment,
  stateProp,
  selected,
  className,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    style: style || "line",
    type: type || "text-icon",
    size: size || "medium",
    alignment: alignment || "auto-width",
    state: stateProp || "enabled",
    selected: selected || false,
  });

  return (
    <div
      className={`tabs-items state-3-${state.state} ${state.style} type-1-${state.type} ${state.alignment} selected-${state.selected} size-3-${state.size} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
    >
      {((state.state === "disabled" && state.style === "line" && state.type === "text-icon") ||
        (state.state === "enabled" && state.style === "line" && state.type === "text-icon") ||
        (state.state === "focus" && state.type === "text-icon") ||
        (state.state === "hover" && state.style === "line" && state.type === "text-icon") ||
        (state.state === "selected" && state.type === "text-icon") ||
        state.state === "skeleton") && (
        <div className="text-overflow">
          {["disabled", "enabled", "focus", "hover", "selected"].includes(state.state) && (
            <div className="tab-label">
              {(state.alignment === "grid-aware" || state.style === "line") && <>{labelText}</>}

              {state.alignment === "auto-width" && state.size === "large" && (
                <div className="tab-label-2">{labelText}</div>
              )}
            </div>
          )}

          {state.state === "skeleton" && (
            <>
              <div className="text-line-padding">
                <div className="text-line" />
              </div>
              <img
                className="border"
                alt="Border"
                src={
                  state.type === "icon-only" && state.size === "medium"
                    ? "/img/border-1.svg"
                    : state.type === "icon-only" && state.size === "large"
                    ? "/img/border-3.svg"
                    : state.alignment === "grid-aware"
                    ? "/img/border-5.svg"
                    : "/img/border-4.svg"
                }
              />
            </>
          )}
        </div>
      )}

      {((state.state === "disabled" && state.style === "line" && state.type === "icon-only") ||
        (state.state === "enabled" && state.style === "line" && state.type === "icon-only") ||
        (state.state === "focus" && state.type === "icon-only") ||
        (state.state === "hover" && state.style === "line" && state.type === "icon-only") ||
        (state.state === "selected" && state.type === "icon-only")) && (
        <Bee6
          className={`${state.size === "large" ? "bee" : "class"}`}
          color={
            state.state === "enabled" || (state.state === "focus" && state.style === "line") ? "#525252" : "#161616"
          }
          fillOpacity={state.state === "disabled" ? "0.25" : undefined}
        />
      )}

      {((state.state === "disabled" && state.style === "contained" && state.type === "text-icon") ||
        (state.state === "enabled" && state.style === "contained" && state.type === "text-icon") ||
        (state.state === "hover" && state.style === "contained" && state.type === "text-icon")) && (
        <div className="text-overflow-wrapper">
          <div className="text-overflow-2">
            {state.alignment === "auto-width" && <div className="tab-label-3">{labelText}</div>}

            {state.alignment === "grid-aware" && <>{labelText}</>}
          </div>
        </div>
      )}

      {((state.state === "disabled" && state.style === "contained" && state.type === "icon-only") ||
        (state.state === "enabled" && state.style === "contained" && state.type === "icon-only") ||
        (state.state === "hover" && state.style === "contained" && state.type === "icon-only")) && (
        <Bee6
          className="bee"
          color={state.state === "hover" ? "#161616" : state.state === "disabled" ? "#8D8D8D" : "#525252"}
        />
      )}

      {state.style === "contained" && ["disabled", "enabled", "hover"].includes(state.state) && (
        <>
          <>
            {divider && (
              <img
                className="img"
                alt="Divider"
                src={
                  state.type === "icon-only"
                    ? "/img/divider-8.svg"
                    : state.type === "text-icon" && state.alignment === "auto-width"
                    ? "/img/divider-6.svg"
                    : state.state === "disabled" && state.alignment === "grid-aware"
                    ? "/img/divider-7.svg"
                    : "/img/divider-4.svg"
                }
              />
            )}
          </>
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

TabsItems.propTypes = {
  hoverDimissible: PropTypes.bool,
  show2NdLabel: PropTypes.bool,
  divider: PropTypes.bool,
  dismissibleIcon: PropTypes.bool,
  labelText: PropTypes.string,
  dismissible: PropTypes.bool,
  icon: PropTypes.bool,
  style: PropTypes.oneOf(["line", "contained"]),
  type: PropTypes.oneOf(["icon-only", "text-icon"]),
  size: PropTypes.oneOf(["large", "medium"]),
  alignment: PropTypes.oneOf(["auto-width", "grid-aware"]),
  stateProp: PropTypes.oneOf(["enabled", "selected", "focus", "hover", "skeleton", "disabled"]),
  selected: PropTypes.bool,
};
