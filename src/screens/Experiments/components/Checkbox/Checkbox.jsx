/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Checkbox23 } from "../../icons/Checkbox23";
import { Checkbox9 } from "../../icons/Checkbox9";
import { CheckboxCheckedFilled7 } from "../../icons/CheckboxCheckedFilled7";
import { CheckboxCheckedFilled8 } from "../../icons/CheckboxCheckedFilled8";
import { CheckboxIndeterminateFilled1 } from "../../icons/CheckboxIndeterminateFilled1";
import { CheckboxIndeterminateFilled2 } from "../../icons/CheckboxIndeterminateFilled2";
import { WarningAltFilled } from "../../icons/WarningAltFilled";
import { WarningFilled1 } from "../../icons/WarningFilled1";
import "./style.css";

export const Checkbox = ({
  warningText = "Warning message goes here",
  helperMessage = false,
  label = true,
  labelText = "Label",
  warningMessage = true,
  errorMessage = true,
  helperText = "Helper text goes here",
  errorText = "Error message goes here",
  valueText = "Checkbox label",
  value = true,
  indented = false,
  stateProp,
  selection,
  className,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    state: stateProp || "enabled",
    selection: selection || "unchecked",
  });

  return (
    <div
      className={`checkbox ${state.state} ${className}`}
      onClick={() => {
        dispatch("click");
      }}
    >
      {["disabled", "enabled", "focus", "invalid", "read-only", "warning"].includes(state.state) && (
        <>
          <>{label && <div className="label">{labelText}</div>}</>
        </>
      )}

      {["disabled", "enabled", "focus", "invalid", "read-only", "warning"].includes(state.state) && (
        <div className="icon-value">
          {((state.selection === "unchecked" && state.state === "disabled") ||
            (state.selection === "unchecked" && state.state === "enabled") ||
            (state.selection === "unchecked" && state.state === "invalid") ||
            (state.selection === "unchecked" && state.state === "read-only") ||
            (state.selection === "unchecked" && state.state === "warning")) && (
            <Checkbox23
              className="instance-node"
              color={state.state === "invalid" ? "#DA1E28" : "#161616"}
              fillOpacity={["disabled", "read-only"].includes(state.state) ? "0.25" : undefined}
            />
          )}

          {state.selection === "checked" && ["disabled", "enabled", "warning"].includes(state.state) && (
            <CheckboxCheckedFilled8
              className="instance-node"
              fillOpacity={state.state === "disabled" ? "0.25" : undefined}
            />
          )}

          {((state.selection === "checked" && state.state === "disabled") ||
            (state.selection === "checked" && state.state === "enabled") ||
            (state.selection === "unchecked" && state.state === "disabled") ||
            (state.selection === "unchecked" && state.state === "enabled") ||
            (state.selection === "unchecked" && state.state === "invalid") ||
            (state.selection === "unchecked" && state.state === "read-only") ||
            state.state === "warning") && (
            <>
              <>
                {value && (
                  <div className="value-margin">
                    <div className="value">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.state === "read-only" && ["checked", "indeterminate"].includes(state.selection) && (
            <>
              <div className={`checkbox-group ${state.selection}`}>
                <img
                  className="checkbox-checked"
                  alt="Checkbox checked"
                  src={
                    state.selection === "indeterminate"
                      ? "../../../asssets/images/Experiments/ElementCreateTarget/checkbox-indeterminate-1.svg"
                      : "../../../asssets/images/Experiments/ElementCreateTarget/checkbox-checked-1.svg"
                  }
                />
              </div>
              <>
                {value && (
                  <div className="value-margin">
                    <div className="text-wrapper">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.selection === "indeterminate" && ["disabled", "enabled"].includes(state.state) && (
            <>
              <CheckboxIndeterminateFilled2
                className="instance-node"
                opacity={state.state === "disabled" ? "0.25" : undefined}
              />
              <>
                {value && (
                  <div className="value-margin">
                    <div className="div">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.selection === "unchecked" && state.state === "focus" && (
            <>
              <Checkbox9 className="instance-node-2" />
              <>
                {value && (
                  <div className="value-margin">
                    <div className="text-wrapper">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.state === "focus" && state.selection === "checked" && (
            <>
              <CheckboxCheckedFilled7 className="instance-node-2" />
              <>
                {value && (
                  <div className="value-margin">
                    <div className="text-wrapper">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.selection === "indeterminate" && state.state === "focus" && (
            <>
              <CheckboxIndeterminateFilled1 className="instance-node-2" />
              <>
                {value && (
                  <div className="value-margin">
                    <div className="text-wrapper">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}

          {state.state === "invalid" && state.selection === "checked" && (
            <>
              <CheckboxCheckedFilled8 className="instance-node" />
              <Checkbox23 className="checkbox-checked" color="#DA1E28" />
              <>
                {value && (
                  <div className="value-margin">
                    <div className="text-wrapper">{valueText}</div>
                  </div>
                )}
              </>
            </>
          )}
        </div>
      )}

      {state.state === "invalid" && (
        <>
          <>
            {errorMessage && (
              <div className="div-2">
                <div className="status-icon">
                  <div className="overlap-group">
                    <div className="fill" />
                    <WarningFilled1 className="instance-node-3" />
                  </div>
                </div>
                <div className="error-message-goes">{errorText}</div>
              </div>
            )}
          </>
        </>
      )}

      {state.state === "warning" && (
        <>
          <>
            {warningMessage && (
              <div className="div-2">
                <div className="status-icon">
                  <div className="overlap-group">
                    <div className="fill-2" />
                    <WarningAltFilled className="instance-node-3" />
                  </div>
                </div>
                <div className="warning-message-goes">{warningText}</div>
              </div>
            )}
          </>
        </>
      )}

      {state.state === "skeleton" && (
        <>
          <Checkbox23 className="instance-node" color="#161616" />
          <div className="value-line" />
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (state.selection === "unchecked" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          selection: "checked",
          state: "enabled",
        };
    }
  }

  if (state.selection === "unchecked" && state.state === "invalid") {
    switch (action) {
      case "click":
        return {
          selection: "checked",
          state: "invalid",
        };
    }
  }

  if (state.selection === "unchecked" && state.state === "warning") {
    switch (action) {
      case "click":
        return {
          selection: "checked",
          state: "warning",
        };
    }
  }

  if (state.selection === "checked" && state.state === "enabled") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "enabled",
        };
    }
  }

  if (state.selection === "checked" && state.state === "invalid") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "invalid",
        };
    }
  }

  if (state.selection === "checked" && state.state === "warning") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "warning",
        };
    }
  }

  if (state.selection === "checked" && state.state === "read-only") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "enabled",
        };
    }
  }

  if (state.selection === "indeterminate" && state.state === "read-only") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "enabled",
        };
    }
  }

  if (state.selection === "unchecked" && state.state === "read-only") {
    switch (action) {
      case "click":
        return {
          selection: "unchecked",
          state: "enabled",
        };
    }
  }

  return state;
}

Checkbox.propTypes = {
  warningText: PropTypes.string,
  helperMessage: PropTypes.bool,
  label: PropTypes.bool,
  labelText: PropTypes.string,
  warningMessage: PropTypes.bool,
  errorMessage: PropTypes.bool,
  helperText: PropTypes.string,
  errorText: PropTypes.string,
  valueText: PropTypes.string,
  value: PropTypes.bool,
  indented: PropTypes.bool,
  stateProp: PropTypes.oneOf(["warning", "skeleton", "enabled", "focus", "read-only", "invalid", "disabled"]),
  selection: PropTypes.oneOf(["checked", "indeterminate", "unchecked"]),
};
