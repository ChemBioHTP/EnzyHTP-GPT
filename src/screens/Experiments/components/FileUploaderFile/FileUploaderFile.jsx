/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { CheckmarkFilled3 } from "../../icons/CheckmarkFilled3";
import { Close } from "../../icons/Close";
// import { Close14 } from "../../icons/Close14";
// import { Close2 } from "../../icons/Close2";
// import { Close3 } from "../../icons/Close3";
// import { Close5 } from "../../icons/Close5";
// import { Close6 } from "../../icons/Close6";
// import { Close7 } from "../../icons/Close7";
import { WarningFilled1 } from "../../icons/WarningFilled1";
import { StatusIcon } from "../StatusIcon";
import "./style.css";

export const FileUploaderFile = ({
  longDesc = "Optional secondary explanation that can go on for two lines.",
  shortDesc = "File exceeds size limit.",
  fileName = "Filename.png",
  size,
  stateProp,
  className,
  statusIconIcon = <WarningFilled1 className="warning-filled" color="#DA1E28" />,
  statusIconState = "warning-red",
  statusIconStateSuccessGreenClassName,
  icon = <Close className="close-14" />,
  divider = "/img/divider-7.svg",
  errorShortClassName,
}) => {
  const [state, dispatch] = useReducer(reducer, {
    size: size || "large",
    state: stateProp || "uploaded",
  });

  return (
    <div
      className={`file-uploader-file ${state.state} ${className}`}
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
    >
      <div className={`file-name size-1-${state.size}`}>
        <div className="file-name-wrapper">
          <div className="file-name-2">{fileName}</div>
        </div>
        {["error-long", "error-short", "focus", "loading", "uploaded"].includes(state.state) && (
          <div className={`icons state-4-${state.state} size-2-${state.size}`}>
            {["error-long", "error-short"].includes(state.state) && (
              <>
                <StatusIcon
                  className={statusIconStateSuccessGreenClassName}
                  highContrast={false}
                  icon={statusIconIcon}
                  state={statusIconState}
                />
                {icon}
              </>
            )}

            {state.state === "uploaded" && state.size === "large" && <Close className="close-2" />}

            {state.state === "uploaded" && state.size === "medium" && <Close className="close-2" />}

            {state.state === "uploaded" && state.size === "small" && <Close className="close-14" />}

            {state.state === "loading" && (
              <div className="loading-animation">
                <div className="loading-base">
                  <div className="ellipse-wrapper">
                    <img className="ellipse" alt="Ellipse" src="/img/ellipse-5.svg" />
                  </div>
                </div>
              </div>
            )}

            {state.state === "focus" && state.size === "large" && <Close className="close-2" />}

            {state.state === "focus" && state.size === "medium" && <Close className="close-2" />}

            {state.size === "small" && state.state === "focus" && <Close className="close-2" />}
          </div>
        )}

        {state.state === "success" && (
          <StatusIcon
            className="status-icon-2"
            highContrast={false}
            icon={<CheckmarkFilled3 className="warning-filled" color="#0F62FE" />}
            state="success-blue"
          />
        )}
      </div>
      {["error-long", "error-short"].includes(state.state) && (
        <>
          <div className="divider-overflow">
            <img className="divider" alt="Divider" src={divider} />
          </div>
          <div className={`error-message size-3-${state.size}`}>
            {state.state === "error-short" && <div className={`error-short-2 ${errorShortClassName}`}>{shortDesc}</div>}

            {state.state === "error-long" && (
              <>
                <div className="error-short-3">{shortDesc}</div>
                <p className="error-description">{longDesc}</p>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  switch (action) {
    case "mouse_leave":
      return {
        ...state,
        state: "success",
      };

    case "mouse_enter":
      return {
        ...state,
        state: "uploaded",
      };
  }

  return state;
}

FileUploaderFile.propTypes = {
  longDesc: PropTypes.string,
  shortDesc: PropTypes.string,
  fileName: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  stateProp: PropTypes.oneOf(["success", "focus", "loading", "uploaded", "error-long", "error-short"]),
  statusIconState: PropTypes.string,
  divider: PropTypes.string,
};
