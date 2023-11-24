/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { AccordionContentSkeleton10 } from "../../icons/AccordionContentSkeleton10";
import { AccordionContentSkeleton5 } from "../../icons/AccordionContentSkeleton5";
import { Chevron4 } from "../../icons/Chevron4";
import { Chevron9 } from "../../icons/Chevron9";
import { Slot } from "../Slot";
import "./style.css";

export const AccordionItem = ({
  slot = true,
  contentText = "The accordion component delivers large amounts of content in a small space through progressive disclosure. The user gets key details about the underlying content and can choose to expand that content within the constraints of the accordion.",
  titleText = "Title of accordion",
  size,
  stateProp,
  alignment,
  flush,
  expanded,
  className,
  hasDiv = true,
  override = <Slot className="slot-instance" size="small" />,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    size: size || "large",
    state: stateProp || "enabled",
    alignment: alignment || "right",
    flush: flush || false,
    expanded: expanded || false,
  });

  return (
    <div
      className={`accordion-item state-10-${state.state} flush-${state.flush} expanded-${state.expanded} size-9-${state.size} ${state.alignment} ${className}`}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
      onClick={() => {
        dispatch("click_3440");
      }}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
    >
      {(!state.expanded || state.state === "skeleton") && (
        <div className="accordion-header">
          {state.state === "skeleton" && (
            <div className="accordion-header-2">
              {state.alignment === "right" && <div className="title-line" />}

              {!state.expanded && <Chevron4 className="instance-node-2" color="#161616" />}

              {state.expanded && <Chevron9 className="instance-node-2" color="#161616" />}

              {state.alignment === "left" && <div className="title-line" />}
            </div>
          )}

          {state.expanded &&
            (!state.flush || state.alignment === "right") &&
            ["left", "right"].includes(state.alignment) && <AccordionContentSkeleton10 className="accordion-content" />}

          {state.expanded && state.flush && state.alignment === "left" && (
            <AccordionContentSkeleton5 className="accordion-content" />
          )}

          {((state.alignment === "right" && state.state === "disabled") ||
            (state.alignment === "right" && state.state === "enabled") ||
            (state.alignment === "right" && state.state === "focus") ||
            (state.alignment === "right" && state.state === "hover")) && (
            <div className="title-of-accordion">{titleText}</div>
          )}

          {(state.state === "disabled" || state.state === "enabled" || (!state.flush && state.state === "focus")) && (
            <Chevron4
              className={`${state.alignment === "left" ? "class-3" : "class-4"}`}
              color="#161616"
              fillOpacity={
                state.state === "disabled" &&
                (state.flush || state.alignment === "left") &&
                ["left", "right"].includes(state.alignment)
                  ? "0.25"
                  : undefined
              }
            />
          )}

          {(state.state === "hover" || (state.flush && state.state === "focus")) && (
            <Chevron4 className={`${state.alignment === "left" ? "class-5" : "class-3"}`} color="#161616" />
          )}

          {state.alignment === "right" &&
            (state.flush || state.state === "hover") &&
            ["focus", "hover"].includes(state.state) && <div className="background" />}

          {((state.alignment === "left" && state.state === "disabled") ||
            (state.alignment === "left" && state.state === "enabled") ||
            (state.alignment === "left" && state.state === "focus") ||
            (state.alignment === "left" && state.state === "hover")) && (
            <div className="title-of-accordion-2">{titleText}</div>
          )}

          {state.alignment === "left" &&
            (state.flush || state.state === "hover") &&
            ["focus", "hover"].includes(state.state) && <div className="background-2" />}
        </div>
      )}

      {((state.expanded && state.state === "disabled") ||
        (state.expanded && state.state === "enabled") ||
        (state.expanded && state.state === "focus") ||
        (state.expanded && state.state === "hover")) && (
        <>
          <div
            className="accordion-header-3"
            onMouseEnter={() => {
              dispatch("mouse_enter_2799");
            }}
            onMouseLeave={() => {
              dispatch("mouse_leave_2799");
            }}
            onClick={() => {
              dispatch("click");
            }}
          >
            {state.alignment === "right" && <div className="title-of-accordion-3">{titleText}</div>}

            {(state.state === "disabled" || state.state === "enabled" || (!state.flush && state.state === "focus")) && (
              <Chevron9
                className={`${state.alignment === "left" ? "class-3" : "class-4"}`}
                color="#161616"
                fillOpacity={state.state === "disabled" ? "0.25" : undefined}
              />
            )}

            {(state.state === "hover" || (state.flush && state.state === "focus")) && (
              <Chevron9 className={`${state.alignment === "left" ? "class-5" : "class-3"}`} color="#161616" />
            )}

            {state.alignment === "right" &&
              (state.flush || state.state === "hover") &&
              ["focus", "hover"].includes(state.state) && <div className="background-3" />}

            {state.alignment === "left" && (
              <div className="title-of-accordion-4">
                {(state.flush || state.state === "enabled") && <>{titleText}</>}

                {!state.flush && ["disabled", "focus", "hover"].includes(state.state) && <>Title of accordion</>}
              </div>
            )}

            {state.alignment === "left" &&
              (state.flush || state.state === "hover") &&
              ["focus", "hover"].includes(state.state) && <div className="focus-border" />}
          </div>
          <div className="accordion-content-2">
            {hasDiv && (
              <div className="the-accordion">
                {((state.alignment === "left" && !state.flush && state.state === "disabled") ||
                  (state.alignment === "left" && !state.flush && state.state === "focus") ||
                  (state.alignment === "left" && !state.flush && state.state === "hover")) && (
                  <p className="text-wrapper-8">
                    The accordion component delivers large amounts of content in a small space through progressive
                    disclosure. The user gets key details about the underlying content and can choose to expand that
                    content within the constraints of the accordion.
                  </p>
                )}

                {((state.alignment === "left" && state.flush && state.state === "disabled") ||
                  (state.alignment === "left" && state.flush && state.state === "focus") ||
                  (state.alignment === "right" && !state.flush && state.state === "hover") ||
                  (state.alignment === "right" && state.state === "disabled") ||
                  (state.alignment === "right" && state.state === "focus") ||
                  (state.flush && state.state === "hover") ||
                  state.state === "enabled") && <p className="text-wrapper-8">{contentText}</p>}
              </div>
            )}

            {((state.alignment === "left" && state.flush && state.state === "disabled") ||
              (state.alignment === "left" && state.flush && state.state === "focus") ||
              (state.alignment === "right" && !state.flush && state.state === "hover") ||
              (state.alignment === "right" && state.state === "disabled") ||
              (state.alignment === "right" && state.state === "focus") ||
              (state.flush && state.state === "hover") ||
              state.state === "enabled") && (
              <>
                <>{slot && <>{override}</>}</>
              </>
            )}

            {((state.alignment === "left" && !state.flush && state.state === "disabled") ||
              (state.alignment === "left" && !state.flush && state.state === "focus") ||
              (state.alignment === "left" && !state.flush && state.state === "hover")) && <>{override}</>}
          </div>
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "large",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "large",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "medium",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "medium",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "small",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "small",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "large",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "large",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "medium",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "medium",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: false,
          size: "small",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "left" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "left",
          expanded: true,
          flush: true,
          size: "small",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "left",
          expanded: false,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "large",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "large",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "medium",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "medium",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "small",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === false &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "small",
          state: "enabled",
        };

      case "click_3440":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "large",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "large" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "large",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "large",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "medium",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "medium" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "medium",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "medium",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === false &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: false,
          size: "small",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: false,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "enabled"
  ) {
    switch (action) {
      case "mouse_enter_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  if (
    state.alignment === "right" &&
    state.expanded === true &&
    state.flush === true &&
    state.size === "small" &&
    state.state === "hover"
  ) {
    switch (action) {
      case "mouse_leave_2799":
        return {
          alignment: "right",
          expanded: true,
          flush: true,
          size: "small",
          state: "enabled",
        };

      case "click":
        return {
          alignment: "right",
          expanded: false,
          flush: true,
          size: "small",
          state: "hover",
        };
    }
  }

  return state;
}

AccordionItem.propTypes = {
  slot: PropTypes.bool,
  contentText: PropTypes.string,
  titleText: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  stateProp: PropTypes.oneOf(["enabled", "focus", "hover", "skeleton", "disabled"]),
  alignment: PropTypes.oneOf(["right", "left"]),
  flush: PropTypes.bool,
  expanded: PropTypes.bool,
  hasDiv: PropTypes.bool,
};
