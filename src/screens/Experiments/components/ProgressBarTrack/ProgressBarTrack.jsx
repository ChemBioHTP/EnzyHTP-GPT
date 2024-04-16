/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const ProgressBarTrack = ({ progress, size, className }) => {
  return (
    <div className={`progress-bar-track ${progress} ${size} ${className}`}>
      {["error", "fifty", "indeterminate", "seventy-five", "success", "twenty-five"].includes(progress) && (
        <div className="track" />
      )}

      {((progress === "error" && size === "small") ||
        progress === "twenty-five") && (
        <>
          <div className="div" />
          <div className="div" />
          <div className="div" />
        </>
      )}

      {((progress === "error" && size === "small") ||
        (progress === "fifty" && size === "small") ) && (
        <>
          <div className="spacer" />
          <div className="div" />
          <div className="div" />
        </>
      )}
      {progress === "fifty" && size === "big" && <div className="spacer-3" />}
    </div>
  );
};

ProgressBarTrack.propTypes = {
  progress: PropTypes.oneOf(["indeterminate", "twenty-five", "zero", "success", "fifty", "seventy-five", "error"]),
  size: PropTypes.oneOf(["small", "big"]),
};
