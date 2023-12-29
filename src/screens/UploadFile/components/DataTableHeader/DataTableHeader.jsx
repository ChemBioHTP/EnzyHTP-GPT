/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { ArrowDown4 } from "../../icons/ArrowDown4";
import { ArrowUp4 } from "../../icons/ArrowUp4";
import { ArrowsVertical4 } from "../../icons/ArrowsVertical4";
import { Resizer } from "../Resizer";
import "./style.css";

export const DataTableHeader = ({
  cellText = "Header",
  size,
  stateProp,
  sorted,
  sortable,
  className,
  resizerResizerClassName,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    size: size || "extra-large",
    state: stateProp || "enabled",
    sorted: sorted || "none",
    sortable: sortable || false,
  });

  return (
    <div
      className={`data-table-header state-10-${state.state} size-20-${state.size} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
    >
      <Resizer className={resizerResizerClassName} />
      <div className="cell-2">
        {state.size === "extra-large" && (
          <>
            <div className="content-2">
              <div className="text-3">{cellText}</div>
              {["hover", "selected"].includes(state.state) && (
                <div className="icon-margin">
                  {state.sorted === "ascending" && <ArrowUp4 className="instance-node-5" />}

                  {state.sorted === "none" && <ArrowsVertical4 className="instance-node-5" />}

                  {state.sorted === "descending" && <ArrowDown4 className="instance-node-5" />}
                </div>
              )}
            </div>
            <div className="min-height-2" />
          </>
        )}

        {["extra-small", "large", "medium", "small"].includes(state.size) && <div className="text-3">{cellText}</div>}

        {((state.size === "extra-small" && state.sorted === "ascending") ||
          (state.size === "large" && state.sorted === "ascending") ||
          (state.size === "medium" && state.sorted === "ascending") ||
          (state.size === "small" && state.sorted === "ascending")) && <ArrowUp4 className="instance-node-5" />}

        {((state.size === "extra-small" && state.sorted === "none" && state.state === "hover") ||
          (state.size === "large" && state.sorted === "none" && state.state === "hover") ||
          (state.size === "medium" && state.sorted === "none" && state.state === "hover") ||
          (state.size === "small" && state.sorted === "none" && state.state === "hover")) && (
          <ArrowsVertical4 className="instance-node-5" />
        )}

        {((state.size === "extra-small" && state.sorted === "descending") ||
          (state.size === "large" && state.sorted === "descending") ||
          (state.size === "medium" && state.sorted === "descending") ||
          (state.size === "small" && state.sorted === "descending")) && <ArrowDown4 className="instance-node-5" />}
      </div>
    </div>
  );
};

function reducer(state, action) {
  if (state.size === "extra-large" && state.sortable === true && state.sorted === "none" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "none",
          state: "hover",
        };
    }
  }

  if (state.size === "extra-large" && state.sortable === true && state.sorted === "none" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "none",
          state: "enabled",
        };
    }
  }

  if (state.size === "large" && state.sortable === true && state.sorted === "none" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "none",
          state: "hover",
        };
    }
  }

  if (state.size === "large" && state.sortable === true && state.sorted === "none" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "medium",
          sortable: true,
          sorted: "none",
          state: "enabled",
        };
    }
  }

  if (state.size === "medium" && state.sortable === true && state.sorted === "none" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "none",
          state: "hover",
        };
    }
  }

  if (state.size === "small" && state.sortable === true && state.sorted === "none" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "small",
          sortable: true,
          sorted: "none",
          state: "hover",
        };
    }
  }

  if (state.size === "small" && state.sortable === true && state.sorted === "none" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "small",
          sortable: true,
          sorted: "none",
          state: "enabled",
        };
    }
  }

  if (state.size === "extra-small" && state.sortable === true && state.sorted === "none" && state.state === "enabled") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "none",
          state: "hover",
        };
    }
  }

  if (state.size === "extra-small" && state.sortable === true && state.sorted === "none" && state.state === "hover") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "none",
          state: "enabled",
        };
    }
  }

  if (
    state.size === "extra-large" &&
    state.sortable === true &&
    state.sorted === "ascending" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "ascending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "extra-large" &&
    state.sortable === true &&
    state.sorted === "ascending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "ascending",
          state: "hover",
        };
    }
  }

  if (state.size === "large" && state.sortable === true && state.sorted === "ascending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "ascending",
          state: "selected",
        };
    }
  }

  if (state.size === "large" && state.sortable === true && state.sorted === "ascending" && state.state === "selected") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "medium",
          sortable: true,
          sorted: "ascending",
          state: "hover",
        };
    }
  }

  if (state.size === "medium" && state.sortable === true && state.sorted === "ascending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "ascending",
          state: "selected",
        };
    }
  }

  if (state.size === "small" && state.sortable === true && state.sorted === "ascending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "small",
          sortable: true,
          sorted: "ascending",
          state: "selected",
        };
    }
  }

  if (state.size === "small" && state.sortable === true && state.sorted === "ascending" && state.state === "selected") {
    switch (action) {
      case "mouse_leave":
        return {
          size: "small",
          sortable: true,
          sorted: "ascending",
          state: "hover",
        };
    }
  }

  if (
    state.size === "extra-small" &&
    state.sortable === true &&
    state.sorted === "ascending" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "ascending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "extra-small" &&
    state.sortable === true &&
    state.sorted === "ascending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "ascending",
          state: "hover",
        };
    }
  }

  if (
    state.size === "extra-large" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "descending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "extra-large" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-large",
          sortable: true,
          sorted: "descending",
          state: "hover",
        };
    }
  }

  if (state.size === "large" && state.sortable === true && state.sorted === "descending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "descending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "large" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "medium",
          sortable: true,
          sorted: "descending",
          state: "hover",
        };
    }
  }

  if (state.size === "medium" && state.sortable === true && state.sorted === "descending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "large",
          sortable: true,
          sorted: "descending",
          state: "selected",
        };
    }
  }

  if (state.size === "small" && state.sortable === true && state.sorted === "descending" && state.state === "hover") {
    switch (action) {
      case "mouse_enter":
        return {
          size: "small",
          sortable: true,
          sorted: "descending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "small" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "small",
          sortable: true,
          sorted: "descending",
          state: "hover",
        };
    }
  }

  if (
    state.size === "extra-small" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "descending",
          state: "selected",
        };
    }
  }

  if (
    state.size === "extra-small" &&
    state.sortable === true &&
    state.sorted === "descending" &&
    state.state === "selected"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          size: "extra-small",
          sortable: true,
          sorted: "descending",
          state: "hover",
        };
    }
  }

  return state;
}

DataTableHeader.propTypes = {
  cellText: PropTypes.string,
  size: PropTypes.oneOf(["large", "extra-large", "extra-small", "small", "medium"]),
  stateProp: PropTypes.oneOf(["hover", "selected", "enabled"]),
  sorted: PropTypes.oneOf(["ascending", "none", "descending"]),
  sortable: PropTypes.bool,
};
