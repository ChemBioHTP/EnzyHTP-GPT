/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Checkbox3 } from "../../icons/Checkbox3";
import { Chevron4 } from "../../icons/Chevron4";
import { Chevron9 } from "../../icons/Chevron9";
import "./style.css";

export const UiShellLeftPanel = ({
  linkText = "Link",
  iconRight = false,
  iconLeft = false,
  type,
  level,
  stateProp,
  selected,
  expanded,
  compact,
  divider,
  className,
  linkIconClassName,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    type: type || "link",
    level: level || "level-1",
    state: stateProp || "enabled",
    selected: selected || false,
    expanded: expanded || false,
    compact: compact || false,
    divider: divider || false,
  });

  return (
    <div
      className={`UI-shell-left-panel state-8-${state.state} divider-${state.divider} compact-${state.compact} ${state.level} selected-2-${state.selected} ${state.type} ${className}`}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onClick={() => {
        dispatch("click");
      }}
    >
      {(state.divider || !state.compact) && (
        <div className={`link-icon ${!state.divider ? linkIconClassName : undefined}`}>
          {!state.divider && <div className="link-2">{linkText}</div>}

          {!state.expanded && state.type === "sub-menu" && (
            <Chevron4
              className="instance-node"
              color={["enabled", "focus"].includes(state.state) ? "#525252" : "#161616"}
              fillOpacity={state.state === "disabled" ? "0.25" : undefined}
            />
          )}

          {state.expanded && (
            <Chevron9
              className="instance-node"
              color={["enabled", "focus"].includes(state.state) ? "#525252" : "#161616"}
              fillOpacity={state.state === "disabled" ? "0.25" : undefined}
            />
          )}
        </div>
      )}

      {state.compact && !state.divider && (
        <Checkbox3
          className="instance-node"
          color={
            ["enabled", "focus"].includes(state.state)
              ? "#525252"
              : ["active", "disabled", "hover", "selected"].includes(state.state)
              ? "#161616"
              : undefined
          }
          fillOpacity={state.state === "disabled" ? "0.25" : undefined}
        />
      )}
    </div>
  );
};

function reducer(state, action) {
  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-2" &&
    state.selected === false &&
    state.state === "enabled" &&
    state.type === "link"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-2",
          selected: false,
          state: "hover",
          type: "link",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-2" &&
    state.selected === false &&
    state.state === "hover" &&
    state.type === "link"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-2",
          selected: false,
          state: "enabled",
          type: "link",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "enabled" &&
    state.type === "link"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "link",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "hover" &&
    state.type === "link"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "enabled",
          type: "link",
        };
    }
  }

  if (
    state.compact === true &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "enabled" &&
    state.type === "compact"
  ) {
    switch (action) {
      case "click":
        return {
          compact: true,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "compact",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "enabled" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "sub-menu",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "hover" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "softly-selected",
          type: "sub-menu",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === false &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "softly-selected" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: false,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "sub-menu",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === true &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "enabled" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: true,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "sub-menu",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === true &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "hover" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          compact: false,
          divider: false,
          expanded: true,
          level: "level-1",
          selected: false,
          state: "softly-selected",
          type: "sub-menu",
        };
    }
  }

  if (
    state.compact === false &&
    state.divider === false &&
    state.expanded === true &&
    state.level === "level-1" &&
    state.selected === false &&
    state.state === "softly-selected" &&
    state.type === "sub-menu"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          compact: false,
          divider: false,
          expanded: true,
          level: "level-1",
          selected: false,
          state: "hover",
          type: "sub-menu",
        };
    }
  }

  return state;
}

UiShellLeftPanel.propTypes = {
  linkText: PropTypes.string,
  iconRight: PropTypes.bool,
  iconLeft: PropTypes.bool,
  type: PropTypes.oneOf(["link", "sub-menu", "divider", "compact"]),
  level: PropTypes.oneOf(["level-2", "level-1"]),
  stateProp: PropTypes.oneOf(["active", "enabled", "selected", "focus", "softly-selected", "hover", "disabled"]),
  selected: PropTypes.bool,
  expanded: PropTypes.bool,
  compact: PropTypes.bool,
  divider: PropTypes.bool,
};
