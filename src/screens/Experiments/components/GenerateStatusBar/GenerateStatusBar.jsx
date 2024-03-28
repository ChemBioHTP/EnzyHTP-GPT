/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Close } from "../../icons/Close";
import { Close97 } from "../../icons/Close97";
import { StatusIcon } from "../StatusIcon";
import "./style.css";

export const GenerateStatusBar = ({
  longDesc = "Optional secondary explanation that can go on for two lines.",
  shortDesc = "File exceeds size limit.",
  fileName = "Filename.png",
  size,
  state,
  className,
}) => {

  return (
    <div
      className={`generate-status-bar ${state} ${className}`}
    >
      <div className={`file-name size-26-${size}`}>
        <div className="file-name-wrapper">
          <div className="file-name-2">{fileName}</div>
        </div>
        {["error-long", "error-short", "focus", "loading", "uploaded"].includes(state) && (
          <div className={`icons state-11-${state} size-27-${size}`}>
            {["error-long", "error-short"].includes(state) && (
              <StatusIcon className="status-icon-instance" highContrast={false} state="warning-red" />
            )}

            {(state === "error-long" ||
              state === "error-short" ||
              (size === "small" && state === "uploaded")) && (
              <Close97 className="close-94" color="#161616" />
            )}

            {state === "loading" && (
              <div className="loading-animation">
                <div className="loading-base">
                  <div className="ellipse-wrapper">
                    <img className="ellipse" alt="Ellipse" src="/img/ellipse-5.svg" />
                  </div>
                </div>
              </div>
            )}

            {state === "focus" && size === "large" && <Close className="close-2" />}

            {state === "focus" && size === "medium" && <Close className="close-2" />}

            {size === "small" && state === "focus" && <Close className="close-2" />}
          </div>
        )}

        {state === "success" && (
          <StatusIcon className="status-icon-instance" highContrast={false} state="success-blue" />
        )}
      </div>
      {["error-long", "error-short"].includes(state) && (
        <>
          <div className="divider-overflow">
            <img className="divider-2" alt="Divider" src="/img/divider-5.svg" />
          </div>
          <div className={`error-message size-28-${size}`}>
            <div className="error-short-2">{shortDesc}</div>
            {state === "error-long" && <p className="error-description">{longDesc}</p>}
          </div>
        </>
      )}
    </div>
  );
};

GenerateStatusBar.propTypes = {
  longDesc: PropTypes.string,
  shortDesc: PropTypes.string,
  fileName: PropTypes.string,
  size: PropTypes.oneOf(["large", "medium", "small"]),
  stateProp: PropTypes.oneOf(["success", "focus", "loading", "uploaded", "error-long", "error-short"]),
};
