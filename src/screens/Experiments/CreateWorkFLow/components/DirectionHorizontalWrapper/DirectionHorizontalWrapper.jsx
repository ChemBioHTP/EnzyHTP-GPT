/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { CheckmarkOutline2 } from "../../icons/CheckmarkOutline2";
import { CircleDash2 } from "../../icons/CircleDash2";
import { Incomplete2 } from "../../icons/Incomplete2";
import { Warning } from "../../icons/Warning";
import { ProgressIndicator } from "../ProgressIndicator";
import "./style.css";

export const DirectionHorizontalWrapper = ({
  optionalLabel = true,
  labelText = "Optional label",
  direction,
  state,
  className,
  icon = <CheckmarkOutline2 className="instance-node-2" />,
  progressIndicatorStepText = "Step",
}) => {
  return (
    <div className={`direction-horizontal-wrapper state-12-${state} ${direction} ${className}`}>
      <div className="content">
        {["completed", "current", "disabled", "error", "incomplete"].includes(state) && (
          <>
            <div className="icon-label">
              {direction === "horizontal" && (
                <>
                  <div className="icon-margin">
                    {["disabled", "incomplete"].includes(state) && (
                      <CircleDash2 className="instance-node-2" opacity={state === "disabled" ? "0.25" : undefined} />
                    )}

                    {state === "error" && <Warning className="instance-node-2" />}

                    {state === "completed" && <CheckmarkOutline2 className="instance-node-2" />}

                    {state === "current" && <Incomplete2 className="instance-node-2" />}
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
                {direction === "horizontal" && <CircleDash2 className="instance-node-2" />}

                {direction === "vertical" && (
                  <>
                    <div className="circle-dash-wrapper">
                      <CircleDash2 className="instance-node-2" />
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
