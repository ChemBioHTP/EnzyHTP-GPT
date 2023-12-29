/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Close } from "../../icons/Close";
import { Search } from "../../icons/Search";
import "./style.css";

export const SearchDefault = ({
  placeholderText = "Search input text",
  queryText = "Typing",
  size,
  stateProp,
  expandable,
  expanded,
  className,
  icon = <Search className="search-7" color="#525252" />,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    size: size || "large",
    state: stateProp || "enabled",
    expandable: expandable || false,
    expanded: expanded || true,
  });

  return (
    <div
      className={`search-default expanded-${state.expanded} state-0-${state.state} expandable-${state.expandable} ${state.size} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onClick={() => {
        dispatch("click");
      }}
    >
      {((state.expanded && state.state === "enabled") ||
        (state.expanded && state.state === "hover") ||
        state.state === "disabled" ||
        state.state === "filled" ||
        state.state === "focus") && (
        <>
          <div className="search-icon">{icon}</div>
          <div className="hide-text-overflow">
            <div className="text">
              {["disabled", "enabled", "hover"].includes(state.state) && <>{placeholderText}</>}

              {["filled", "focus"].includes(state.state) && <>{queryText}</>}
            </div>
          </div>
        </>
      )}

      {["disabled", "filled", "focus"].includes(state.state) && (
        <div className="clear-icon">
          <Close className="search-7" fillOpacity={state.state === "disabled" ? "0.25" : undefined} />
        </div>
      )}

      {(!state.expanded || state.state === "skeleton") && (
        <div className="search-base">
          {!state.expanded && ["large", "medium"].includes(state.size) && <>{icon}</>}

          {!state.expanded && state.size === "small" && <Search className="search-7" color="#525252" />}
        </div>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (state.expandable === false && state.expanded === true && state.size === "large" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: false,
          expanded: true,
          size: "large",
          state: "filled",
        };
    }
  }

  if (state.expandable === false && state.expanded === true && state.size === "medium" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: false,
          expanded: true,
          size: "medium",
          state: "filled",
        };
    }
  }

  if (state.expandable === false && state.expanded === true && state.size === "small" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: false,
          expanded: true,
          size: "small",
          state: "filled",
        };
    }
  }

  if (state.expandable === true && state.expanded === true && state.size === "large" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: true,
          expanded: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === true && state.size === "medium" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: true,
          expanded: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === true && state.size === "small" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          expandable: true,
          expanded: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "large" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          expandable: true,
          expanded: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "large" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          expandable: true,
          expanded: false,
          size: "large",
          state: "enabled",
        };

      case "click":
        return {
          expandable: true,
          expanded: true,
          size: "large",
          state: "enabled",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "medium" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          expandable: true,
          expanded: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "medium" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          expandable: true,
          expanded: false,
          size: "medium",
          state: "enabled",
        };

      case "click":
        return {
          expandable: true,
          expanded: true,
          size: "medium",
          state: "enabled",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "small" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          expandable: true,
          expanded: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (state.expandable === true && state.expanded === false && state.size === "small" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          expandable: true,
          expanded: false,
          size: "small",
          state: "enabled",
        };

      case "click":
        return {
          expandable: true,
          expanded: true,
          size: "small",
          state: "enabled",
        };
    }
  }

  return state;
}

SearchDefault.propTypes = {
  placeholderText: PropTypes.string,
  queryText: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  stateProp: PropTypes.oneOf(["enabled", "filled", "focus", "hover", "skeleton", "disabled"]),
  expandable: PropTypes.bool,
  expanded: PropTypes.bool,
};
