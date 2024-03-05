/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { ArrowRight } from "../../icons/ArrowRight";
import { Checkbox3 } from "../../icons/Checkbox3";
import { CheckboxCheckedFilled } from "../../icons/CheckboxCheckedFilled";
import { CheckmarkFilled } from "../../icons/CheckmarkFilled";
import { Chevron4 } from "../../icons/Chevron4";
import { Chevron9 } from "../../icons/Chevron9";
import { Error } from "../../icons/Error";
import { Button } from "../Button";
import "./style.css";

export const Tile = ({
  margin = false,
  descText = "Description",
  showDesc = true,
  slot = false,
  showTitle = true,
  titleText = "Title",
  accessible,
  type,
  stateProp,
  className,
  divClassName,
  divClassNameOverride,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    accessible: accessible || false,
    type: type || "base",
    state: stateProp || "enabled",
  });

  return (
    <div
      className={`tile state-17-${state.state} ${state.type} accessible-${state.accessible} ${className}`}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
    >
      <div className="content-3">
        {((state.state === "disabled" && state.type === "single-select") ||
          (state.state === "enabled" && state.type === "single-select") ||
          (state.state === "focus" && state.type === "single-select") ||
          (state.state === "hover" && state.type === "single-select") ||
          state.type === "base" ||
          state.type === "clickable" ||
          state.type === "expandable-interactive" ||
          state.type === "expandable") && (
          <div className="content-4">
            {showTitle && (
              <div className={`title ${["base", "single-select"].includes(state.type) ? divClassName : undefined}`}>
                {titleText}
              </div>
            )}

            {showDesc && (
              <div
                className={`description ${
                  ["base", "single-select"].includes(state.type) ? divClassNameOverride : undefined
                }`}
              >
                {descText}
              </div>
            )}
          </div>
        )}

        {((state.state === "enabled-selected" && state.type === "single-select") ||
          (state.state === "focus-selected" && state.type === "single-select") ||
          (state.state === "hover-selected" && state.type === "single-select") ||
          state.type === "multi-select") && (
          <div className="title-description-wrapper">
            <div className="title-description">
              {showTitle && <div className="title-2">{titleText}</div>}

              {showDesc && <div className="description-2">{descText}</div>}
            </div>
          </div>
        )}

        {state.type === "single-select" &&
          ["enabled-selected", "focus-selected", "hover-selected"].includes(state.state) && (
            <CheckmarkFilled className="instance-node-3" color="#161616" />
          )}

        {((state.state === "disabled" && state.type === "multi-select") ||
          (state.state === "enabled" && state.type === "multi-select") ||
          (state.state === "focus" && state.type === "multi-select") ||
          (state.state === "hover" && state.type === "multi-select")) && (
          <Checkbox3
            className="instance-node-3"
            color="#161616"
            fillOpacity={state.state === "disabled" ? "0.25" : undefined}
          />
        )}

        {state.type === "multi-select" &&
          ["enabled-selected", "focus-selected", "hover-selected"].includes(state.state) && (
            <CheckboxCheckedFilled className="instance-node-3" />
          )}
      </div>
      {["clickable", "expandable-interactive", "expandable"].includes(state.type) && (
        <div className="interactive-icon">
          {state.type === "clickable" && (
            <div className="icon-4">
              {["enabled", "focus", "hover"].includes(state.state) && <ArrowRight className="instance-node-4" />}

              {state.state === "disabled" && <Error className="instance-node-4" />}
            </div>
          )}

          {["expandable-interactive", "expandable"].includes(state.type) && (
            <Button
              className="button-2"
              override={
                ["enabled", "focus", "hover"].includes(state.state) ? (
                  <Chevron9 className="instance-node-5" color="#161616" />
                ) : ["enabled-expanded", "focus-expanded", "hover-expanded"].includes(state.state) ? (
                  <Chevron4 className="instance-node-5" color="#161616" />
                ) : undefined
              }
              size="large"
              stateProp={
                state.type === "expandable" ||
                (state.state === "enabled-expanded" && state.type === "expandable-interactive") ||
                (state.state === "enabled" && state.type === "expandable-interactive")
                  ? "enabled"
                  : state.type === "expandable-interactive" && ["hover-expanded", "hover"].includes(state.state)
                  ? "hover"
                  : state.type === "expandable-interactive" && ["focus-expanded", "focus"].includes(state.state)
                  ? "focus"
                  : undefined
              }
              style="ghost"
              type="icon-only"
            />
          )}
        </div>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (state.accessible === false && state.state === "enabled" && state.type === "clickable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "clickable",
        };
    }
  }

  if (state.accessible === false && state.state === "hover" && state.type === "clickable") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "focus",
          type: "clickable",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled" && state.type === "clickable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "clickable",
        };
    }
  }

  if (state.accessible === true && state.state === "hover" && state.type === "clickable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "clickable",
        };
    }
  }

  if (state.accessible === true && state.state === "focus" && state.type === "clickable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "clickable",
        };
    }
  }

  if (state.accessible === false && state.state === "enabled" && state.type === "single-select") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "single-select",
        };
    }
  }

  if (state.accessible === false && state.state === "hover" && state.type === "single-select") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: false,
          state: "enabled",
          type: "single-select",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled" && state.type === "single-select") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover",
          type: "single-select",
        };
    }
  }

  if (state.accessible === true && state.state === "hover" && state.type === "single-select") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "enabled",
          type: "single-select",
        };
    }
  }

  if (state.accessible === false && state.state === "disabled" && state.type === "single-select") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "single-select",
        };
    }
  }

  if (state.accessible === true && state.state === "disabled" && state.type === "single-select") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover",
          type: "single-select",
        };
    }
  }

  if (state.accessible === false && state.state === "enabled" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === false && state.state === "hover" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: false,
          state: "enabled",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === false && state.state === "enabled" && state.type === "expandable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover",
          type: "expandable",
        };
    }
  }

  if (state.accessible === false && state.state === "hover" && state.type === "expandable") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: false,
          state: "enabled",
          type: "expandable",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === true && state.state === "hover" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "enabled",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled" && state.type === "expandable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover",
          type: "expandable",
        };
    }
  }

  if (state.accessible === true && state.state === "hover" && state.type === "expandable") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "enabled",
          type: "expandable",
        };
    }
  }

  if (state.accessible === false && state.state === "enabled-expanded" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover-expanded",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === false && state.state === "hover-expanded" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: false,
          state: "enabled-expanded",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === false && state.state === "enabled-expanded" && state.type === "expandable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: false,
          state: "hover-expanded",
          type: "expandable",
        };
    }
  }

  if (state.accessible === false && state.state === "hover-expanded" && state.type === "expandable") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: false,
          state: "enabled-expanded",
          type: "expandable",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled-expanded" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover-expanded",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === true && state.state === "hover-expanded" && state.type === "expandable-interactive") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "enabled-expanded",
          type: "expandable-interactive",
        };
    }
  }

  if (state.accessible === true && state.state === "enabled-expanded" && state.type === "expandable") {
    switch (action) {
      case "mouse_enter":
        return {
          accessible: true,
          state: "hover-expanded",
          type: "expandable",
        };
    }
  }

  if (state.accessible === true && state.state === "hover-expanded" && state.type === "expandable") {
    switch (action) {
      case "mouse_leave":
        return {
          accessible: true,
          state: "enabled-expanded",
          type: "expandable",
        };
    }
  }

  return state;
}

Tile.propTypes = {
  margin: PropTypes.bool,
  descText: PropTypes.string,
  showDesc: PropTypes.bool,
  slot: PropTypes.bool,
  showTitle: PropTypes.bool,
  titleText: PropTypes.string,
  accessible: PropTypes.bool,
  type: PropTypes.oneOf(["expandable-interactive", "multi-select", "single-select", "base", "expandable", "clickable"]),
  stateProp: PropTypes.oneOf([
    "enabled-selected",
    "focus-selected",
    "hover-expanded",
    "enabled",
    "focus",
    "hover-selected",
    "hover",
    "focus-expanded",
    "enabled-expanded",
    "disabled",
  ]),
};
