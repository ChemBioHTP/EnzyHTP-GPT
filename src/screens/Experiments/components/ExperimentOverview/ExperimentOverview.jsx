/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Resizer } from "../Resizer";
import "./style.css";

export const ExperimentOverview = ({
  heading = true,
  type,
  stateProp,
  className,
  text = "Target metrics",
  frameClassName,
  text1 = "Please provide the prompt and run the experiment.",
  divClassName,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    type: type || "tags",
    state: stateProp || "default",
    heading: heading || false,
  });

  return (
    <div
      className={`experiment-overview ${state.type} heading-${state.heading} state-12-${state.state} ${className}`}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
    >
      {(!state.heading || state.type === "flow" || state.type === "tags") && (
        <>
          <div className="target-metrics">
            {!state.heading && <>{text}</>}

            {state.heading && (
              <>
                <div className="target-metrics-2">{text}</div>
                <p className="text-wrapper-6">In progress: waiting for inputs</p>
              </>
            )}
          </div>
          <div className={`frame-desc ${frameClassName}`}>
            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-4">
                      {state.type === "flow" && <>Remove water</>}

                      {state.type === "tags" && <>Esomething F (EF)</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && <img className="line-2" alt="Line" src="/img/line-11-3.svg" />}

            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-4">
                      {state.type === "tags" && <>Full name (SPI)</>}

                      {state.type === "flow" && <>Loop fixing</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && <img className="line-2" alt="Line" src="/img/line-11-3.svg" />}

            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-5">
                      {state.type === "tags" && <>MMPB/GBSA binding</>}

                      {state.type === "flow" && <>Protonate</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && <img className="line-2" alt="Line" src="/img/line-11-3.svg" />}

            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-5">
                      {state.type === "flow" && <>Mutate</>}

                      {state.type === "tags" && <>Trajectories</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && <img className="line-2" alt="Line" src="/img/line-11-3.svg" />}

            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-5">
                      {state.type === "flow" && <>Parameterization</>}

                      {state.type === "tags" && <>AI metrics</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && <img className="line-2" alt="Line" src="/img/line-11-3.svg" />}

            {["flow", "tags"].includes(state.type) && (
              <div className="tag-content-wrapper">
                <div className="tag-content">
                  <div className="label-3">
                    <div className="label-5">
                      {state.type === "flow" && <>MD simulation</>}

                      {state.type === "tags" && <>Stability</>}
                    </div>
                    <Resizer className="resizer-instance" />
                  </div>
                </div>
              </div>
            )}

            {state.type === "flow" && (
              <>
                <img className="line-2" alt="Line" src="/img/line-11-3.svg" />
                <div className="tag-content-wrapper">
                  <div className="tag-content">
                    <div className="label-3">
                      <div className="label-5">Calculate metrics</div>
                      <Resizer className="resizer-instance" />
                    </div>
                  </div>
                </div>
                <img className="line-2" alt="Line" src="/img/line-11-3.svg" />
                <div className="tag-content-wrapper">
                  <div className="tag-content">
                    <div className="label-3">
                      <div className="label-5">Stability</div>
                      <Resizer className="resizer-instance" />
                    </div>
                  </div>
                </div>
                <img className="line-2" alt="Line" src="/img/line-11-3.svg" />
                <div className="tag-content-wrapper">
                  <div className="tag-content">
                    <div className="label-3">
                      <div className="label-5">Stability</div>
                      <Resizer className="resizer-instance" />
                    </div>
                  </div>
                </div>
                <img className="line-2" alt="Line" src="/img/line-11-3.svg" />
                <div className="tag-content-wrapper">
                  <div className="tag-content">
                    <div className="label-3">
                      <div className="label-5">Stability</div>
                      <Resizer className="resizer-instance" />
                    </div>
                  </div>
                </div>
                <img className="line-2" alt="Line" src="/img/line-11-3.svg" />
                <div className="tag-content-wrapper">
                  <div className="tag-content">
                    <div className="label-3">
                      <div className="label-5">Stability</div>
                      <Resizer className="resizer-instance" />
                    </div>
                  </div>
                </div>
              </>
            )}

            {state.type === "text" && <p className="text-wrapper-10">{text1}</p>}
          </div>
        </>
      )}

      {state.heading && state.type === "text" && (
        <>
          <div className="target-metrics-3">{text}</div>
          <p className="text-wrapper-6">In progress: waiting for inputs</p>
          <p className={`please-provide-the ${divClassName}`}>{text1}</p>
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (state.heading === false && state.state === "default" && state.type === "tags") {
    switch (action) {
      case "mouse_enter":
        return {
          heading: false,
          state: "hover",
          type: "tags",
        };
    }
  }

  if (state.heading === false && state.state === "hover" && state.type === "tags") {
    switch (action) {
      case "mouse_leave":
        return {
          heading: false,
          state: "hover",
          type: "flow",
        };
    }
  }

  if (state.heading === false && state.state === "default" && state.type === "flow") {
    switch (action) {
      case "mouse_enter":
        return {
          heading: false,
          state: "hover",
          type: "tags",
        };
    }
  }

  if (state.heading === false && state.state === "hover" && state.type === "flow") {
    switch (action) {
      case "mouse_enter":
        return {
          heading: false,
          state: "hover",
          type: "tags",
        };
    }
  }

  return state;
}

ExperimentOverview.propTypes = {
  heading: PropTypes.bool,
  type: PropTypes.oneOf(["tags", "flow", "text"]),
  stateProp: PropTypes.oneOf(["hover", "default"]),
  heading1: PropTypes.bool,
  text: PropTypes.string,
  text1: PropTypes.string,
};
