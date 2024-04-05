/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { WarningAltFilled } from "../../icons/WarningAltFilled";
import { WarningFilled1 } from "../../icons/WarningFilled1";
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
              <>{showLabel && <div className={`label-text ${state}`}>{labelText}</div>}</>
            </>
          )}

          {(state === "skeleton" || (size === "large" && state === "active")) && (
            <div className={`div filled-${filled} state-${state}`}>{filled && <>{labelText}</>}</div>
          )}
        </div>
      )}

      {state === "skeleton" && <div className={`text-input-box size-0-${size}`} />}

      {["active", "disabled", "enabled", "focus"].includes(state) && (
        <DeprecatedText
          backgroundClassName={DEPRECATEDTextBackgroundClassName}
          className="DEPRECATED-text-input-base"
          divClassName={`${(state === "focus" || (!filled && state === "enabled")) && "class"} ${filled && "class-2"} ${
            state === "disabled" && "class-3"
          }`}
          hasIcon={false}
          initialInputText={DEPRECATEDTextInputText}
          size={size === "medium" ? "medium" : size === "small" ? "small" : "large"}
          textOverflowClassName="DEPRECATED-text-instance"
        />
      )}

      {["active", "disabled", "enabled", "focus", "skeleton"].includes(state) && (
        <>
          <>
            {showHelper && (
              <div className={`helper-text-line state-0-${state}`}>
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
            divClassName={`${filled ? "class-2" : "class"}`}
            inputText={DEPRECATEDTextInputText}
            override={state === "error" ? <WarningFilled1 className="instance-node" color="#DA1E28" /> : undefined}
            size={size === "medium" ? "medium" : size === "small" ? "small" : "large"}
            statusIconIcon={
              state === "warning" ? <WarningAltFilled className="instance-node" color="#F1C21B" /> : undefined
            }
            visible={state === "warning" ? false : undefined}
            visible1={state === "error" ? false : undefined}
          />
          <div className={`warning-message-goes state-1-${state}`}>
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
