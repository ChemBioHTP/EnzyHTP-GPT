/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useState, useRef, useEffect } from 'react';
import { WarningAltFilled } from "../../icons/WarningAltFilled";
import { WarningFilled } from "../../icons/WarningFilled";
import "./style.css";

export const TextInputDefault = ({
  countText = "0/100",
  labelText = "Label",
  showLabel = true,
  showCount = false,
  inputText = "Input text",
  placeholderText = "Placeholder text (optional)",
  errorText = "Error message goes here",
  showHelper = true,
  helperText = "Optional helper text",
  warningText = "Warning message goes here",
  size,
  state,
  textFilled,
  className,
  spacerClassName,
  backgroundClassName,
  inputType = "text",
  onInputChange,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    const value = event.target.value;
    setInputValue(value);
    onInputChange(value);
  };
  
  
  return (
    <div className={`text-input-default ${state} ${className}`}>
      {["active", "disabled", "enabled", "focus", "read-only", "error", "warning"].includes(state) && (
        <div className="label-character">
          {showLabel && (
            <div className="label-margin">{showLabel && <div className="label-text">{labelText}</div>}</div>
          )}

          <div className={`spacer ${spacerClassName}`} />
        </div>
      )}
      {["active", "disabled", "enabled", "focus", "read-only", "error", "warning"].includes(state) && (
        <div className={["error", "warning"].includes(state) ? `text-input state-5-${state} size-0-${size}`:`text-input state-0-${state} ${size} text-filled-${textFilled}`}>
          {size === "large" && (!textFilled || state === "read-only") && ["enabled", "read-only","error"].includes(state) && (
            <>
              <div className="status-icon">
                <div className="overlap-group">
                  <div className="fill" />
                  {state === "warning" && <WarningAltFilled className="instance-node" />}

                  {state === "error" && <WarningFilled className="instance-node" />}
                </div>
              </div>

              <div className="text-overflow">

                <input
                  className={`input text-filled-2-${textFilled}`}
                  placeholder={state === "enabled" && !textFilled ? placeholderText : textFilled ? inputText : undefined}
                  type={inputType}
                  value={inputValue}
                  onChange={handleInputChange}
                />
                <div className="spacer-2" />

              </div>
              
              {["active", "disabled", "enabled", "focus", "read-only"].includes(state) && (
                <div className={`background ${backgroundClassName}`} />
              )}
              
            </>
          )}

          {((size === "large" && state === "active") ||
            (size === "large" && state === "disabled") ||
            (size === "large" && state === "enabled" && textFilled) ||
            (size === "large" && state === "focus") ||
            size === "medium" ||
            size === "small") && (
            <div className="placeholder-text-wrapper">
              <div className="placeholder-text">
                {(state === "disabled" || state === "focus" || (!textFilled && state === "enabled")) && (
                  <>{placeholderText}</>
                )}

                {textFilled && <>{inputText}</>}

                {state === "read-only" && !textFilled && <>No input text</>}
              </div>
            </div>
          )}
        </div>
      )}

      {state === "skeleton" && (
        <>
          <>
            {showLabel && (
              <div className="label-skeleton">
                <div className="label-text-line" />
              </div>
            )}
          </>
          <div className={`text-input-box size-${size}`} />
        </>
      )}

      {["active", "disabled", "enabled", "focus", "read-only", "skeleton", "warning", "error"].includes(state) && (
        <>
          <div className="helper-text-margin">
            {showHelper && (
              <div className="optional-helper-text">
                {["active", "disabled", "enabled", "focus", "read-only"].includes(state) && <>{helperText}</>}
              </div>
            )}
            {["warning", "error"].includes(state) &&(
              <div className="warning-message-goes">
                {state === "warning" && <>{warningText}</>}

                {state === "error" && <>{errorText}</>}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

TextInputDefault.propTypes = {
  countText: PropTypes.string,
  labelText: PropTypes.string,
  showLabel: PropTypes.bool,
  showCount: PropTypes.bool,
  inputText: PropTypes.string,
  placeholderText: PropTypes.string,
  errorText: PropTypes.string,
  showHelper: PropTypes.bool,
  helperText: PropTypes.string,
  warningText: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  state: PropTypes.oneOf(["warning", "active", "enabled", "focus", "read-only", "skeleton", "error", "disabled"]),
  textFilled: PropTypes.bool,
  inputType: PropTypes.string,
};
