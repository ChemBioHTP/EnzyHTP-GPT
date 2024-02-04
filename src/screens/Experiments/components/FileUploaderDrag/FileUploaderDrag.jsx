/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const FileUploaderDrag = ({ helperText = "Drag and drop files here or click to upload", state, className }) => {
  return (
    <div className={`file-uploader-drag state-${state} ${className}`}>
      <div className="description-wrapper">
        <p className="description">{helperText}</p>
      </div>
    </div>
  );
};

FileUploaderDrag.propTypes = {
  helperText: PropTypes.string,
  state: PropTypes.oneOf(["disabled", "drag-hover", "focus", "enabled"]),
};
