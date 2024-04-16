/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const ProgressBarTrack = ({ progress, className }) => {
  return (
    <div className={`progress-bar-track ${progress} ${className}`}>
      {["error", "fifty", "indeterminate", "seventy-five", "success", "twenty-five"].includes(progress) && (
        <div className="track" />
      )}

      {(progress === "zero") && (
        <>
          <div className="div" />
          <div className="div" />
          <div className="div" />
          <div className="div" />
        </>
      )}

      {(progress === "twenty-five") && (
        <>
          <div className="div" />
          <div className="div" />
          <div className="div" />
        </>
      )}

      {(progress === "fifty") && (
        <>
          <div className="spacer" />
          <div className="div" />
          <div className="div" />
        </>
      )}
      {(progress === "seventy-five") && (
        <>
          <div className="spacer" />
          <div className="spacer" />
          <div className="div" />
        </>
      )}
      {(progress === "success") && (
        <>
          <div className="spacer" />
          <div className="spacer" />
          <div className="spacer" />
        </>
      )}
      
    </div>
  );
};

ProgressBarTrack.propTypes = {
  progress: PropTypes.oneOf(["indeterminate", "twenty-five", "zero", "success", "fifty", "seventy-five", "error"]),
};
