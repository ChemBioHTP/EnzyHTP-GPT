/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { CheckmarkOutline1 } from "../../icons/CheckmarkOutline1";
import { CircleDash6 } from "../../icons/CircleDash6";
import { Incomplete1 } from "../../icons/Incomplete1";
import { Warning1 } from "../../icons/Warning1";
import { ProgressIndicator } from "../ProgressIndicator";
import "./style.css";

export const DirectionHorizontalWrapper = ({
  optionalLabel = true,
  labelText = "Optional label",
  direction,
  state,
  className,
  icon = <Incomplete1 className="instance-node-3" />,
  progressIndicatorStepText = "Step",
}) => {
  return (
    <div className={`direction-horizontal-wrapper state-13-${state} ${direction} ${className}`}>
      <div className="content">
        {["completed", "current", "disabled", "error", "incomplete"].includes(state) && (
          <>
            <div className="icon-label">
              {direction === "horizontal" && (
                <>
                  <div className="icon-margin">
                    {["disabled", "incomplete"].includes(state) && (
                      <CircleDash6 className="instance-node-3" opacity={state === "disabled" ? "0.25" : undefined} />
                    )}

                    {state === "error" && <Warning1 className="instance-node-3" />}

                    {state === "completed" && <CheckmarkOutline1 className="instance-node-3" />}

                    {state === "current" && <Incomplete1 className="instance-node-3" />}
                  </div>
                  <ProgressIndicator
                    className="progress-indicator-step-label-base"
                    stateProp={state === "disabled" ? "disabled" : "enabled"}
                    stepText="Step"
                    tooltip={false}
                  />
                </>
              )}

              {direction === "vertical" && (
                <>
                  <div className="icon-label-2">
                    <div className="icon-margin">{icon}</div>
                    <ProgressIndicator
                      className="progress-indicator-step-label-base"
                      stateProp={state === "disabled" ? "disabled" : "enabled"}
                      stepText={progressIndicatorStepText}
                      tooltip={false}
                    />
                  </div>
                  <div className="optional-label">
                    {optionalLabel && <div className="optional-label-2">{labelText}</div>}
                  </div>
                </>
              )}
            </div>
            <div className="optional-label-3">
              {direction === "horizontal" && (
                <>
                  <>{optionalLabel && <div className="optional-label-4">{labelText}</div>}</>
                </>
              )}
            </div>
          </>
        )}
      </div>
      <div className="min-width">
        {state === "skeleton" && (
          <>
            <div className="content-2">
              <div className="icon-margin-2">
                {direction === "horizontal" && <CircleDash6 className="instance-node-3" />}

                {direction === "vertical" && (
                  <>
                    <div className="circle-dash-wrapper">
                      <CircleDash6 className="instance-node-3" />
                    </div>
                    <div className="text-margin">
                      <div className="text-line-2" />
                    </div>
                  </>
                )}
              </div>
              <div className="text-margin-2">{direction === "horizontal" && <div className="text-line-2" />}</div>
            </div>
            <div className="min-width-2" />
          </>
        )}
      </div>
    </div>
  );
};

DirectionHorizontalWrapper.propTypes = {
  optionalLabel: PropTypes.bool,
  labelText: PropTypes.string,
  direction: PropTypes.oneOf(["vertical", "horizontal"]),
  state: PropTypes.oneOf(["completed", "incomplete", "current", "skeleton", "error", "disabled"]),
  progressIndicatorStepText: PropTypes.string,
};
