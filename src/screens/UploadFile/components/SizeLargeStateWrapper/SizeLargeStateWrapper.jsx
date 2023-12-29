/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { DeprecatedText } from "../DeprecatedText";
import "./style.css";

export const SizeLargeStateWrapper = ({
  labelText = "Label",
  showLabel = true,
  errorText = "Error message goes here",
  showHelper = true,
  helperText = "Helper text",
  warningText = "Warning message goes here",
  size,
  state,
  filled,
  className,
  DEPRECATEDTextBackgroundClassName,
  DEPRECATEDTextInputText = "Input text",
}) => {
  return (
    <div className={`size-large-state-wrapper ${className}`}>
      {showLabel && (
        <div className="label-margin">
          {((size === "medium" && state === "active") ||
            (size === "small" && state === "active") ||
            state === "disabled" ||
            state === "enabled" ||
            state === "error" ||
            state === "focus" ||
            state === "warning") && (
            <>
              <>{showLabel && <div className={`label-text state-12-${state}`}>{labelText}</div>}</>
            </>
          )}

          {(state === "skeleton" || (size === "large" && state === "active")) && (
            <div className={`label-text-2 filled-${filled} state-${state}`}>{filled && <>{labelText}</>}</div>
          )}
        </div>
      )}

      {state === "skeleton" && <div className={`text-input-box size-24-${size}`} />}

      {["active", "disabled", "enabled", "focus"].includes(state) && (
        <DeprecatedText
          backgroundClassName={DEPRECATEDTextBackgroundClassName}
          className="DEPRECATED-text-input-base"
          divClassName={`${(state === "focus" || (!filled && state === "enabled")) && "class-842"} ${
            filled && "class-843"
          } ${state === "disabled" && "class-844"}`}
          hasIcon={false}
          inputText={DEPRECATEDTextInputText}
          size={size === "medium" ? "medium" : size === "small" ? "small" : "large"}
          textOverflowClassName="DEPRECATED-text-instance"
        />
      )}

      {["active", "disabled", "enabled", "focus", "skeleton"].includes(state) && (
        <>
          <>
            {showHelper && (
              <div className={`helper-text-line state-13-${state}`}>
                {["active", "disabled", "enabled", "focus"].includes(state) && <>{helperText}</>}
              </div>
            )}
          </>
        </>
      )}

      {["error", "warning"].includes(state) && (
        <>
          <DeprecatedText
            backgroundClassName={DEPRECATEDTextBackgroundClassName}
            className="DEPRECATED-text-input-base"
            divClassName={`${filled ? "class-843" : "class-842"}`}
            inputText={DEPRECATEDTextInputText}
            size={size === "medium" ? "medium" : size === "small" ? "small" : "large"}
            visible={state === "warning" ? false : undefined}
            visible1={state === "error" ? false : undefined}
          />
          <div className={`warning-message-goes state-14-${state}`}>
            {state === "warning" && <>{warningText}</>}

            {state === "error" && <>{errorText}</>}
          </div>
        </>
      )}
    </div>
  );
};

SizeLargeStateWrapper.propTypes = {
  labelText: PropTypes.string,
  showLabel: PropTypes.bool,
  errorText: PropTypes.string,
  showHelper: PropTypes.bool,
  helperText: PropTypes.string,
  warningText: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  state: PropTypes.oneOf(["warning", "active", "enabled", "focus", "skeleton", "error", "disabled"]),
  filled: PropTypes.bool,
  DEPRECATEDTextInputText: PropTypes.string,
};
